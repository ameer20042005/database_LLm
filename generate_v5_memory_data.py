"""Generate v5 Category B: memory-with-long-system-prompt (Iraqi Arabic).

Highest-priority production failure mode: with no system prompt, the model
recalls the customer's name/need perfectly; with a long (279+ token) system
prompt present, it invents a different name. This module forces the long
end of the system-prompt range and stress-tests name recall across a
variable number of distractor turns:

  - long system prompt (300-800 tokens) + catalog
  - name given at turn 1, OR at "turn 3" (after 1-2 generic turns), OR never
    given at all (~18% of examples -> the honest "ما گتلي اسمك" answer)
  - 3-10 distractor turns of ordinary catalog Q&A
  - recall test: explicit ("تتذكر شنو اسمي؟") or implicit (assistant
    naturally drops the name back into a normal answer)

Each record carries a `meta: {customer_name, name_given, recall_turn}` field
so validate_v5.py can check recall correctness deterministically instead of
re-deriving it via NLP.

Run:
    python generate_v5_memory_data.py --n 1500
"""
import argparse
import json
import random
from pathlib import Path

from generate_v5_grounded_data import (
    CUSTOMER_NAMES,
    DATA_DIR,
    build_catalog,
    build_services,
    build_system,
    flatten_types,
    load_bank,
    service_profile_for,
    user_ask_item,
    assistant_answer_item,
)

HAJJI_NAMES = ["حجي جاسم", "حجي عبود", "حجية أم كرار", "حجي كاظم", "حجية زهراء", "حجي أبو تراب"]
NAME_POOL = CUSTOMER_NAMES + HAJJI_NAMES

INTRO_WITH_NAME_T1 = [
    "هلو، اسمي {name} وأدور {type}",
    "هلا، أني {name}، عندكم {plural}؟",
    "سلام، أني {name}، أريد {type}",
]
INTRO_NO_NAME = [
    "هلو، أدور {type}",
    "هلا، عندكم {plural}؟",
    "سلام، أريد {type}",
]
NAME_LATER = [
    "بالمناسبة اسمي {name}",
    "آه نسيت اگلك، أني {name}",
    "صراحة اسمي {name}",
]
NAME_ACK = ["زين {name}، تفضل", "هلا {name}، تدلل", "زين، حاضر {name}"]

EXPLICIT_RECALL_Q = ["تتذكر شنو اسمي؟", "تعرف اسمي؟", "گلتلك اسمي مو؟", "تذكر اسمي لو نسيته؟"]
EXPLICIT_RECALL_A = ["إي والله، اسمك {name}", "اكو، انت {name}", "اسمك {name} والله، ما نسيت"]
EXPLICIT_RECALL_A_NONAME = [
    "والله ما گتلي اسمك، بس أعرف تدور على {plural}",
    "ما گتلي اسمك للأسف، بس متذكر طلبك {plural}",
    "لا، ما تذكر اسمك، بس أعرف شنو تريد",
]

IMPLICIT_RECALL_Q = ["زين شنو آخر سعر؟", "خلص، بيش صار؟", "تمام، آخذه", "زين، شكد الإجمالي؟"]


def answer_with_name(item, name, rng):
    base = assistant_answer_item(item, rng)
    style = rng.choice(["هلا {name}، {base}", "أهلين {name}، {base}", "{base}، تدلل {name}"])
    return style.format(name=name, base=base)


def implicit_recall_reply(item, name, rng):
    base = assistant_answer_item(item, rng)
    style = rng.choice(["تدلل {name}، {base}", "أوكي {name}، {base}", "{base}، تكرم {name}"])
    return style.format(name=name, base=base)


def gen_memory(all_types, rng):
    items = build_catalog(all_types, rng, k=rng.randint(5, 6))
    target = rng.choice(items)
    other_items = [it for it in items if it is not target]
    profile = service_profile_for(items)
    services, services_text = build_services(rng, profile)
    system = build_system(items, services_text, rng, long=True)
    messages = [{"role": "system", "content": system}]

    name_given = rng.random() >= 0.18
    name = rng.choice(NAME_POOL) if name_given else None
    name_at_turn1 = name_given and rng.random() < 0.6

    if name_given and name_at_turn1:
        intro = rng.choice(INTRO_WITH_NAME_T1).format(name=name, type=target["type"], plural=target["plural"])
        messages.append({"role": "user", "content": intro})
        messages.append({"role": "assistant", "content": answer_with_name(target, name, rng)})
    else:
        intro = rng.choice(INTRO_NO_NAME).format(type=target["type"], plural=target["plural"])
        messages.append({"role": "user", "content": intro})
        messages.append({"role": "assistant", "content": assistant_answer_item(target, rng)})
        if name_given:
            # name revealed a couple turns later ("turn 3")
            filler = rng.choice(other_items) if other_items else target
            messages.append({"role": "user", "content": user_ask_item(filler, rng)})
            messages.append({"role": "assistant", "content": assistant_answer_item(filler, rng)})
            messages.append({"role": "user", "content": rng.choice(NAME_LATER).format(name=name)})
            messages.append({"role": "assistant", "content": rng.choice(NAME_ACK).format(name=name)})

    n_distract = rng.randint(3, 10)
    distractor_pool = other_items or items
    last_item = None
    for _ in range(n_distract):
        choices = [it for it in distractor_pool if it is not last_item] or distractor_pool
        it = rng.choice(choices)
        last_item = it
        messages.append({"role": "user", "content": user_ask_item(it, rng)})
        reply = assistant_answer_item(it, rng)
        if name_given and rng.random() < 0.25:
            reply = rng.choice(["{name}، {r}", "{r}، {name}"]).format(name=name, r=reply)
        messages.append({"role": "assistant", "content": reply})

    if not name_given:
        messages.append({"role": "user", "content": rng.choice(EXPLICIT_RECALL_Q)})
        messages.append({"role": "assistant", "content": rng.choice(EXPLICIT_RECALL_A_NONAME).format(plural=target["plural"])})
    elif rng.random() < 0.5:
        messages.append({"role": "user", "content": rng.choice(EXPLICIT_RECALL_Q)})
        messages.append({"role": "assistant", "content": rng.choice(EXPLICIT_RECALL_A).format(name=name)})
    else:
        messages.append({"role": "user", "content": rng.choice(IMPLICIT_RECALL_Q)})
        messages.append({"role": "assistant", "content": implicit_recall_reply(target, name, rng)})

    recall_turn = len(messages) - 1
    meta = {"customer_name": name, "name_given": name_given, "recall_turn": recall_turn}
    return messages, "grounded_catalog_memory", meta


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1500)
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--val-ratio", type=float, default=0.05)
    ap.add_argument("--out-train", default=str(DATA_DIR / "v5" / "memory_train.jsonl"))
    ap.add_argument("--out-val", default=str(DATA_DIR / "v5" / "memory_val.jsonl"))
    args = ap.parse_args()

    rng = random.Random(args.seed)
    all_types = flatten_types(load_bank())

    records = []
    for i in range(args.n):
        msgs, cat, meta = gen_memory(all_types, rng)
        records.append({
            "id": f"v5_memory_{i + 1:05d}", "category": cat, "dialect": "iraqi_arabic",
            "messages": msgs, "meta": meta, "source_file": "generate_v5_memory_data.py",
        })

    rng.shuffle(records)
    n_val = int(len(records) * args.val_ratio)
    val_records, train_records = records[:n_val], records[n_val:]

    Path(args.out_train).parent.mkdir(parents=True, exist_ok=True)
    with open(args.out_train, "w", encoding="utf-8") as f:
        for r in train_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(args.out_val, "w", encoding="utf-8") as f:
        for r in val_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"total: {len(records)} (train {len(train_records)} / val {len(val_records)})")


if __name__ == "__main__":
    main()
