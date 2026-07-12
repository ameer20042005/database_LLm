"""Shared text-quality checks for the v5 pipeline (audit_corpus.py + validate_v5.py).

Placeholder/template-leak detection, Arabic normalization, mixed-script
corruption detection, dialect-keyword coverage, sentence/token counting.
Kept dependency-light: only `regex` (for Unicode script properties) and,
optionally, `transformers` (for real token counts, with a heuristic
fallback if the tokenizer can't be downloaded).
"""
import re
import sys

import regex

# ---------------------------------------------------------------------------
# Placeholder / template-leak detection
# ---------------------------------------------------------------------------
PLACEHOLDER_PATTERNS = [
    re.compile(r'\{\{[^{}]*\}\}'),           # {{...}}
    re.compile(r'\{[a-zA-Z_][a-zA-Z0-9_]*\}'),  # {var}
    re.compile(r'<<[^<>]*>>'),               # <<...>>
    re.compile(r'\[[A-Z_]{2,}\]'),           # [PRODUCT], [NAME]
    re.compile(r'\$[a-zA-Z_][a-zA-Z0-9_]*'), # $var
    re.compile(r'%s'),                       # %s
]


def find_placeholders(text):
    found = []
    for pat in PLACEHOLDER_PATTERNS:
        found.extend(pat.findall(text))
    return found


# ---------------------------------------------------------------------------
# Arabic normalization (for hashing / near-dup shingling)
# ---------------------------------------------------------------------------
_TASHKEEL = regex.compile(r'[ؐ-ًؚ-ٰٟۖ-ۭࣣ-ࣿ]')
_ALEF_VARIANTS = re.compile(r'[إأآا]')
_WS = re.compile(r'\s+')


def normalize_arabic(text):
    text = _TASHKEEL.sub('', text or '')
    text = _ALEF_VARIANTS.sub('ا', text)
    text = text.replace('ة', 'ه')
    text = text.replace('ى', 'ي')
    text = _WS.sub(' ', text).strip()
    return text


def shingles(text, k=3):
    words = normalize_arabic(text).split()
    if len(words) < k:
        return {' '.join(words)} if words else set()
    return {' '.join(words[i:i + k]) for i in range(len(words) - k + 1)}


# ---------------------------------------------------------------------------
# Mixed-script corruption (e.g. Hangul/Han glyphs stuck mid-word in Arabic)
# ---------------------------------------------------------------------------
_FOREIGN_SCRIPT = regex.compile(
    r'[\p{Script=Hangul}\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}'
    r'\p{Script=Cyrillic}\p{Script=Devanagari}\p{Script=Thai}\p{Script=Hebrew}]'
)
_ARABIC_SCRIPT = regex.compile(r'\p{Script=Arabic}')


def has_corrupted_mixed_script(text):
    for token in (text or '').split():
        if _FOREIGN_SCRIPT.search(token) and _ARABIC_SCRIPT.search(token):
            return True
    return False


# ---------------------------------------------------------------------------
# Dialect keyword coverage
# ---------------------------------------------------------------------------
DIALECT_KEYWORDS = [
    # task-given core lexicon
    "شنو", "شلون", "هسه", "اكو", "أكو", "ماكو", "زين", "خوش", "شكد", "چا",
    "هيچي", "باچر", "هواي", "عدنا", "گله", "أگدر", "اگدر", "تكدر",
    # IRAQI_DIALECT_REFERENCE.md additions
    "هلا", "بالهنا", "شلونك", "تمسى على خير", "يدوم عزك", "باجي", "حجي",
    "حجية", "عمو", "هسا", "باكر", "كلش", "چيف", "شنوه", "شوكت", "بيش",
    "والله", "صدك", "گال", "گالوا", "دووس", "دوس", "چاي", "گاع", "فدوة",
    "فداك", "ما قصرت", "زبون معميل", "بالجملة", "دلال", "مسوي سعر",
    "نزل السعر", "تقسيط", "شخبارك", "وياك", "خلص", "تفضل", "گلي", "گلتلك",
    "أبد", "كلشي", "دگة", "هاي", "ذيج", "اجه", "اجت", "شتريد", "أريدك",
    # additions found missing while validating generated v5 output
    "عندنا", "إي", "بس", "مو", "وين", "تسلم", "ماشي", "يخليك", "يعافيك",
    "العافية", "لسه",
]
_DIALECT_KEYWORDS_NORM = [normalize_arabic(k) for k in DIALECT_KEYWORDS]


def contains_dialect_keyword(text):
    norm = normalize_arabic(text)
    return any(k in norm for k in _DIALECT_KEYWORDS_NORM)


# ---------------------------------------------------------------------------
# Sentence splitting (Arabic-aware: only '.', '!', '؟' end a sentence — '،' does not)
# ---------------------------------------------------------------------------
_SENT_SPLIT = re.compile(r'[.!؟]+')


def split_sentences(text):
    parts = [p.strip() for p in _SENT_SPLIT.split(text or '') if p.strip()]
    if parts:
        return parts
    return [text.strip()] if (text or '').strip() else []


# ---------------------------------------------------------------------------
# Number extraction (for verbatim-price-in-system-prompt checks)
# ---------------------------------------------------------------------------
_NUM_RE = re.compile(r'\d[\d,٬]*')


def extract_numbers(text):
    nums = []
    for m in _NUM_RE.findall(text or ''):
        cleaned = m.replace(',', '').replace('٬', '')
        try:
            nums.append(int(cleaned))
        except ValueError:
            continue
    return nums


_DINAR_RE = re.compile(r'(\d[\d,٬]*)\s*دينار')


def extract_dinar_amounts(text):
    """Numbers specifically tagged as dinar amounts (immediately followed by
    'دينار'), as opposed to *any* digit sequence - a bare digit run in Arabic
    sales chat is often a model number ("بي إم دبليو 520"), an area ("200
    متر"), or similar, not a price, and shouldn't be held to the "must be
    grounded in the system prompt" rule that genuinely only applies to
    prices."""
    amounts = []
    for m in _DINAR_RE.finditer(text or ''):
        cleaned = m.group(1).replace(',', '').replace('٬', '')
        try:
            amounts.append(int(cleaned))
        except ValueError:
            continue
    return amounts


# ---------------------------------------------------------------------------
# Token counting — real tokenizer if reachable, heuristic fallback otherwise
# ---------------------------------------------------------------------------
_TOKENIZER_NAME = "ameer4wisam/gemma-iraqi-finetune-v2"
_tokenizer = None  # None = not yet attempted, False = attempted & failed


def _get_tokenizer():
    global _tokenizer
    if _tokenizer is None:
        try:
            from transformers import AutoTokenizer
            _tokenizer = AutoTokenizer.from_pretrained(_TOKENIZER_NAME)
        except Exception as e:  # noqa: BLE001 - any failure -> heuristic fallback
            _tokenizer = False
            print(
                f"[text_checks] WARNING: could not load tokenizer '{_TOKENIZER_NAME}' "
                f"({e!r}); falling back to a heuristic char/2.7 token-count estimate.",
                file=sys.stderr,
            )
    return _tokenizer


def count_tokens(text):
    tok = _get_tokenizer()
    if tok:
        return len(tok.encode(text or '', add_special_tokens=False))
    return max(1, round(len(text or '') / 2.7))
