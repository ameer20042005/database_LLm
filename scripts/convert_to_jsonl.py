"""Convert iraqi_training_data/*.json into training-ready JSONL
(chat "messages" format), split into train/validation sets.

The train split is sharded into multiple files so no single file
approaches GitHub's 100 MB push limit.

Run:
    python convert_to_jsonl.py
"""
import json
import random
from pathlib import Path

FOLDER = Path(__file__).parent / "iraqi_training_data"
SEED = 42
VAL_RATIO = 0.05
MAX_SHARD_BYTES = 40 * 1024 * 1024  # ~40 MB per train shard, well under GitHub's 100 MB limit

# category files to merge; iraqi_train_04_cars.json is skipped because
# iraqi_train_04_cars_plus_scraped.json already contains its 10,000 records
# plus 832 extra scraped ones.
CATEGORY_FILES = [
    "iraqi_train_01_electronics.json",
    "iraqi_train_02_food.json",
    "iraqi_train_03_clothes.json",
    "iraqi_train_04_cars_plus_scraped.json",
    "iraqi_train_05_realestate.json",
    "iraqi_train_06_furniture.json",
    "iraqi_train_07_services.json",
    "iraqi_train_08_daily.json",
    "iraqi_train_09_social.json",
    "iraqi_train_10_mixed.json",
    "iraqi_train_11_health.json",
    "iraqi_train_12_education.json",
    "iraqi_train_13_government.json",
    "iraqi_train_14_restaurant.json",
    "iraqi_train_15_transport.json",
    "iraqi_train_16_sports.json",
    "iraqi_train_17_family.json",
    "iraqi_train_18_occasions.json",
    "iraqi_train_19_neighborhood.json",
    "iraqi_train_20_work.json",
]

QA_FILE = "train.json"


def load_category_files():
    records = []
    for name in CATEGORY_FILES:
        # short source tag, e.g. "01_electronics", "04_cars", "10_mixed"
        tag = name.replace("iraqi_train_", "").replace("_plus_scraped", "").replace(".json", "")
        path = FOLDER / name
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
        for item in data:
            messages = item.get("messages", [])
            if not messages or any(not m.get("content", "").strip() for m in messages):
                continue
            records.append({
                # original ids collide across category files (same id, different
                # conversation content), so prefix with the source tag to keep
                # every record's id globally unique.
                "id": f"{tag}__{item['id']}",
                "category": item.get("category"),
                "dialect": item.get("dialect", "iraqi_arabic"),
                "messages": messages,
                "source_file": name,
            })
    return records


def load_qa_file():
    path = FOLDER / QA_FILE
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    records = []
    for i, item in enumerate(data, start=1):
        q = (item.get("Question") or "").strip()
        a = (item.get("Answer") or "").strip()
        if not q or not a:
            continue
        topic = item.get("Topic", "general")
        records.append({
            "id": f"qa_{topic.lower()}_{i:05d}",
            "category": f"qa_{topic.lower()}" if topic else "qa_general",
            "dialect": "iraqi_arabic",
            "messages": [
                {"role": "user", "content": q},
                {"role": "assistant", "content": a},
            ],
            "formality": item.get("Formality"),
            "date": item.get("Date"),
            "source_file": QA_FILE,
        })
    return records


def main():
    records = load_category_files() + load_qa_file()

    ids_seen = set()
    for r in records:
        if r["id"] in ids_seen:
            raise ValueError(f"duplicate id found: {r['id']}")
        ids_seen.add(r["id"])

    random.Random(SEED).shuffle(records)

    n_val = int(len(records) * VAL_RATIO)
    val_records = records[:n_val]
    train_records = records[n_val:]

    # remove any previously generated output files (e.g. an old unsharded
    # iraqi_train.jsonl) so stale files don't linger alongside new shards.
    for stale in FOLDER.glob("iraqi_train*.jsonl"):
        stale.unlink()

    val_path = FOLDER / "iraqi_val.jsonl"
    with open(val_path, "w", encoding="utf-8") as f:
        for r in val_records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    lines = [json.dumps(r, ensure_ascii=False) + "\n" for r in train_records]
    shards = []
    shard_lines, shard_bytes = [], 0
    for line in lines:
        shard_lines.append(line)
        shard_bytes += len(line.encode("utf-8"))
        if shard_bytes >= MAX_SHARD_BYTES:
            shards.append(shard_lines)
            shard_lines, shard_bytes = [], 0
    if shard_lines:
        shards.append(shard_lines)

    train_paths = []
    for i, shard_lines in enumerate(shards, start=1):
        path = FOLDER / f"iraqi_train_part{i:02d}.jsonl"
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(shard_lines)
        train_paths.append(path)

    print(f"total records: {len(records)}")
    print(f"train: {len(train_records)} -> {len(train_paths)} shard(s):")
    for p in train_paths:
        print(f"  {p} ({p.stat().st_size / 1024 / 1024:.1f} MB)")
    print(f"val:   {len(val_records)} -> {val_path} ({val_path.stat().st_size / 1024 / 1024:.1f} MB)")

    by_cat = {}
    for r in records:
        by_cat[r["category"]] = by_cat.get(r["category"], 0) + 1
    print("\nby category:")
    for cat, n in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {n}")


if __name__ == "__main__":
    main()
