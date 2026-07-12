# v4 Corpus Audit Report

Seed: 42

## Counts

| Stage | Train | Val | Total |
|---|---|---|---|
| raw | 163429 | 10330 | 173759 |
| after placeholder removal (2640 removed) | 160962 | 10157 | 171119 |
| after exact-dup removal (train 0, val 0 removed) | 160962 | 10157 | 171119 |
| after near-dup removal (11272 removed) | 150874 | | |
| after leakage fix (0 val records dropped) | 150874 | 8973 | 159847 |
| after corruption removal (0 removed) | final surviving = 159847 | | |

## Grounding-risk classification (v4 has no system-prompt/catalog grounding)

- **Price-bearing, excluded from v5 mix**: 83634 (52.3%) — assistant turn states a concrete dinar price with no system catalog to ground it; would re-teach memorized/hallucinated pricing.
- **Dialect-kept, folded into v5 mix**: 76213 (47.7%) — daily talk, social, greetings, negotiation phrasing without concrete numbers; contributes dialect diversity only.

## Assistant-turn token-length histogram

| Bucket | Before (raw v4) | After (dialect_kept) |
|---|---|---|
| 0-10 | 121593 | 52906 |
| 11-20 | 265757 | 119053 |
| 21-40 | 127618 | 41467 |
| 41-80 | 6499 | 799 |
| 81+ | 0 | 0 |

## Outputs

- `data/v5/flagged_placeholders.jsonl`
- `data/v5/flagged_corrupted.jsonl`
- `data/v5/v4_price_bearing_excluded.jsonl` (excluded from final mix)
- `data/v5/v4_dialect_kept.jsonl` (folded into final mix by generate_v5.py)