"""Generate v5 clarification/disambiguation training data (Iraqi Arabic).

Step 9 of the v6 plan: the model must learn to ask before assuming when the
customer's request is ambiguous, instead of guessing a spec/brand/quantity
and quoting a price for the wrong item. Missing scenario that broke the
"ask before assuming" rule:

    زبون: أريد اثنين
    بائع: اثنين طن واحد لو طن ونص؟
    زبون: طن ونص
    بائع: [السعر من الكتالوج]

Every example still starts with a system prompt + injected catalog (same
persona/header/footer pools as generate_v5_grounded_data.py) so the model
never learns to memorize specific products - only the "ask, then copy from
context" behavior. Four ambiguity axes, mixed by ratio:

  1. spec   (35%) - type has 2+ possible specs/sizes in the catalog, customer
                     asks generically, assistant must ask which one
  2. brand  (30%) - type available in 2+ brands, assistant must ask which
  3. qty    (20%) - ambiguous quantity phrasing ("أريد اثنين") that collides
                     with a spec name (e.g. طنين), or a bare "give me two"
                     without saying which model both should be
  4. region (15%) - customer asks about delivery without naming an area

Run:
    python generate_v5_clarify_data.py --n 400
"""
import argparse
import random
from pathlib import Path

from generate_v5_grounded_data import (
    DATA_DIR,
    Q_GENERIC,
    GREET_PREFIX,
    REGIONS,
    Q_DELIVERY_ASK,
    A_DELIVERY_CLARIFY,
    Q_REGION_ANSWER,
    A_DELIVERY_CONFIRM,
    build_catalog,
    build_services,
    build_system,
    catalog_text,  # noqa: F401  (re-exported for parity/debugging)
    chain_followups,
    domain_group_of,
    flatten_types,
    join_name,
    load_bank,
    pick_price,
    fmt_price,
    service_profile_for,
    user_ask_item,
    assistant_answer_item,
)

TON_KEYWORD = "طن"

Q_AMBIG_QTY_TON = ["أريد اثنين", "عطني اثنين", "أبيه اثنين", "أريد وحدة اثنين"]
CLARIFY_QTY_TON_Q = [
    "اثنين شنو تقصد، {opts}؟",
    "زين، تقصد {opts}؟",
    "اثنين، {opts}؟ گلي",
    "وضحلي شنو تريد، {opts}؟",
]

Q_AMBIG_QTY_GENERIC = ["أريد فدين {plural}", "أبيه اثنين {plural}", "عطني وحدتين {plural}"]
CLARIFY_QTY_GENERIC_Q = [
    "الفدين نفس الموديل لو مختلفين؟ عدنا {opts}",
    "أي موديل تريد للفدين زين، {opts}؟",
    "خليهم نفس النوع؟ عدنا {opts}، شتختار؟",
]

CLARIFY_SPEC_Q = [
    "شنو الحجم اللي تريد، {opts}؟",
    "عدنا {opts}، شتفضل؟",
    "تريد {opts} زين؟",
    "عدنا {opts} من هذا النوع، أيهم تختار؟",
]

CLARIFY_BRAND_Q = [
    "شنو الماركة اللي تريد، {opts}؟",
    "عدنا {opts}، شتفضل؟",
    "{opts}؟ گلي شتريد بالضبط",
    "عدنا {opts} من هذا الصنف، أيهم أحسنلك؟",
]

CUSTOMER_RESOLVE = ["{val}", "أريد {val}", "خليها {val}", "الـ{val}", "{val} زين"]


def join_options(vals):
    if len(vals) == 1:
        return vals[0]
    if len(vals) == 2:
        return f"{vals[0]} لو {vals[1]}"
    return "، ".join(vals[:-1]) + f" لو {vals[-1]}"


def make_item_fixed(type_name, cfg, rng, brand, spec, domain=None):
    price = pick_price(cfg["price_range"], rng)
    warranty = rng.choice(cfg["warranty"]) if cfg["warranty"] else None
    name = join_name(type_name, brand, spec)
    return {"type": type_name, "brand": brand, "spec": spec, "name": name,
            "price": price, "warranty": warranty, "plural": cfg["plural"], "domain": domain}


def build_variant_items(type_name, cfg, rng, n, vary, domain=None):
    if vary == "spec":
        specs = rng.sample(cfg["specs"], min(n, len(cfg["specs"])))
        brand = rng.choice(cfg["brands"])
        return [make_item_fixed(type_name, cfg, rng, brand, s, domain=domain) for s in specs]
    brands = rng.sample(cfg["brands"], min(n, len(cfg["brands"])))
    spec = rng.choice(cfg["specs"])
    return [make_item_fixed(type_name, cfg, rng, b, spec, domain=domain) for b in brands]


def add_distractors(items, type_name, all_types, rng):
    # restrict distractors to the anchor type's own domain group so a
    # catalog never mixes unrelated shops (e.g. a car next to an AC)
    anchor_domain = next((d for d, t, c in all_types if t == type_name), None)
    group = domain_group_of(anchor_domain) if anchor_domain else None
    other_types = [t for t in all_types if t[1] != type_name and (group is None or t[0] in group)]
    k = rng.choice([0, 0, 1, 2])
    if k and other_types:
        items = items + build_catalog(other_types, rng, k=min(k, len(other_types)))
    rng.shuffle(items)
    return items


def gen_clarify_spec(all_types, rng):
    candidates = [(d, t, c) for d, t, c in all_types if len(c["specs"]) >= 2] or all_types
    domain, type_name, cfg = rng.choice(candidates)
    n = rng.choice([2, 2, 3])
    variants = build_variant_items(type_name, cfg, rng, n, vary="spec", domain=domain)
    items = add_distractors(list(variants), type_name, all_types, rng)
    profile = service_profile_for(items)
    services, services_text = build_services(rng, profile)
    system = build_system(items, services_text, rng)
    messages = [{"role": "system", "content": system}]

    prefix = rng.choice(GREET_PREFIX)
    ask = rng.choice(Q_GENERIC).format(plural=cfg["plural"])
    messages.append({"role": "user", "content": prefix + ask})

    opts = join_options([v["spec"] for v in variants])
    messages.append({"role": "assistant", "content": rng.choice(CLARIFY_SPEC_Q).format(opts=opts)})

    chosen = rng.choice(variants)
    messages.append({"role": "user", "content": rng.choice(CUSTOMER_RESOLVE).format(val=chosen["spec"])})
    messages.append({"role": "assistant", "content": assistant_answer_item(chosen, rng)})

    chain_followups(messages, items, chosen, rng)
    return messages, "grounded_catalog_clarify_spec"


def gen_clarify_brand(all_types, rng):
    candidates = [(d, t, c) for d, t, c in all_types if len(c["brands"]) >= 2] or all_types
    domain, type_name, cfg = rng.choice(candidates)
    n = rng.choice([2, 2, 3])
    variants = build_variant_items(type_name, cfg, rng, n, vary="brand", domain=domain)
    items = add_distractors(list(variants), type_name, all_types, rng)
    profile = service_profile_for(items)
    services, services_text = build_services(rng, profile)
    system = build_system(items, services_text, rng)
    messages = [{"role": "system", "content": system}]

    prefix = rng.choice(GREET_PREFIX)
    ask = rng.choice(Q_GENERIC).format(plural=cfg["plural"])
    messages.append({"role": "user", "content": prefix + ask})

    opts = join_options([v["brand"] for v in variants])
    messages.append({"role": "assistant", "content": rng.choice(CLARIFY_BRAND_Q).format(opts=opts)})

    chosen = rng.choice(variants)
    messages.append({"role": "user", "content": rng.choice(CUSTOMER_RESOLVE).format(val=chosen["brand"])})
    messages.append({"role": "assistant", "content": assistant_answer_item(chosen, rng)})

    chain_followups(messages, items, chosen, rng)
    return messages, "grounded_catalog_clarify_brand"


def gen_clarify_qty(all_types, rng):
    ton_candidates = [(d, t, c) for d, t, c in all_types if any(TON_KEYWORD in s for s in c["specs"])]
    if ton_candidates and rng.random() < 0.6:
        domain, type_name, cfg = rng.choice(ton_candidates)
        ton_specs = [s for s in cfg["specs"] if TON_KEYWORD in s]
        n = min(2, len(ton_specs))
        chosen_specs = rng.sample(ton_specs, n)
        brand = rng.choice(cfg["brands"])
        variants = [make_item_fixed(type_name, cfg, rng, brand, s, domain=domain) for s in chosen_specs]
        items = add_distractors(list(variants), type_name, all_types, rng)
        profile = service_profile_for(items)
        services, services_text = build_services(rng, profile)
        system = build_system(items, services_text, rng)
        messages = [{"role": "system", "content": system}]
        messages.append({"role": "user", "content": rng.choice(Q_AMBIG_QTY_TON)})
        opts = join_options([v["spec"] for v in variants])
        messages.append({"role": "assistant", "content": rng.choice(CLARIFY_QTY_TON_Q).format(opts=opts)})
    else:
        multi_spec = [(d, t, c) for d, t, c in all_types if len(c["specs"]) >= 2] or all_types
        domain, type_name, cfg = rng.choice(multi_spec)
        variants = build_variant_items(type_name, cfg, rng, 2, vary="spec", domain=domain)
        items = add_distractors(list(variants), type_name, all_types, rng)
        profile = service_profile_for(items)
        services, services_text = build_services(rng, profile)
        system = build_system(items, services_text, rng)
        messages = [{"role": "system", "content": system}]
        messages.append({"role": "user", "content": rng.choice(Q_AMBIG_QTY_GENERIC).format(plural=cfg["plural"])})
        opts = join_options([v["spec"] for v in variants])
        messages.append({"role": "assistant", "content": rng.choice(CLARIFY_QTY_GENERIC_Q).format(opts=opts)})

    chosen = rng.choice(variants)
    messages.append({"role": "user", "content": rng.choice(CUSTOMER_RESOLVE).format(val=chosen["spec"])})
    messages.append({"role": "assistant", "content": assistant_answer_item(chosen, rng)})

    chain_followups(messages, items, chosen, rng)
    return messages, "grounded_catalog_clarify_qty"


def gen_clarify_region(all_types, rng):
    # delivery doesn't make sense for property sales (you don't deliver an
    # apartment) — exclude عقارات from this scenario entirely
    deliverable_types = [t for t in all_types if t[0] != "عقارات"] or all_types
    items = build_catalog(deliverable_types, rng)
    target = rng.choice(items)
    profile = service_profile_for(items)
    services, services_text = build_services(rng, profile)
    system = build_system(items, services_text, rng)
    messages = [{"role": "system", "content": system}]
    messages.append({"role": "user", "content": user_ask_item(target, rng)})
    messages.append({"role": "assistant", "content": assistant_answer_item(target, rng)})
    messages.append({"role": "user", "content": rng.choice(Q_DELIVERY_ASK)})
    messages.append({"role": "assistant", "content": rng.choice(A_DELIVERY_CLARIFY)})
    region = rng.choice(REGIONS)
    messages.append({"role": "user", "content": rng.choice(Q_REGION_ANSWER).format(region=region)})
    messages.append({"role": "assistant", "content": rng.choice(A_DELIVERY_CONFIRM).format(region=region)})
    chain_followups(messages, items, target, rng, exclude={"region"})
    return messages, "grounded_catalog_clarify_region"


RATIOS = {"spec": 0.35, "brand": 0.30, "qty": 0.20, "region": 0.15}
GENERATORS = {
    "spec": gen_clarify_spec,
    "brand": gen_clarify_brand,
    "qty": gen_clarify_qty,
    "region": gen_clarify_region,
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=400, help="total examples to generate")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--val-ratio", type=float, default=0.1)
    ap.add_argument("--out-train", default=str(DATA_DIR / "iraqi_train_v5_clarify.jsonl"))
    ap.add_argument("--out-val", default=str(DATA_DIR / "iraqi_val_v5_clarify.jsonl"))
    args = ap.parse_args()

    rng = random.Random(args.seed)
    bank = load_bank()
    all_types = flatten_types(bank)

    counts = {k: round(args.n * v) for k, v in RATIOS.items()}
    drift = args.n - sum(counts.values())
    counts["spec"] += drift

    records = []
    counters = {k: 0 for k in RATIOS}

    def next_id(pattern):
        counters[pattern] += 1
        return f"v5_clarify_{pattern}_{counters[pattern]:05d}"

    for pattern, gen_fn in GENERATORS.items():
        for _ in range(counts[pattern]):
            msgs, cat = gen_fn(all_types, rng)
            records.append({
                "id": next_id(pattern), "category": cat, "dialect": "iraqi_arabic",
                "messages": msgs, "source_file": "generate_v5_clarify_data.py",
            })

    rng.shuffle(records)
    n_val = int(len(records) * args.val_ratio)
    val_records = records[:n_val]
    train_records = records[n_val:]

    import json
    with open(args.out_train, "w", encoding="utf-8") as f:
        for r in train_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    with open(args.out_val, "w", encoding="utf-8") as f:
        for r in val_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    print(f"total: {len(records)}  (train {len(train_records)} / val {len(val_records)})")
    print("by pattern:", counts)
    print(f"train -> {args.out_train}")
    print(f"val   -> {args.out_val}")


if __name__ == "__main__":
    main()
