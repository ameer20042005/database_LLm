#!/usr/bin/env bash
# End-to-end v5 dataset build: audit v4 -> generate v5 -> validate v5.
# Run from the repo root:
#   ./build_v5.sh [--seed 42]
set -e

SEED="${1:-42}"
if [ "$SEED" = "--seed" ]; then
    SEED="$2"
fi

echo "== installing requirements =="
pip install -r requirements-v5.txt --quiet

echo "== Phase 1: auditing v4 corpus (seed=$SEED) =="
python audit_corpus.py --seed "$SEED"

echo "== Phase 2: generating v5 dataset (seed=$SEED) =="
python generate_v5.py --seed "$SEED"

echo "== Phase 3: validating v5 dataset =="
python validate_v5.py

echo "== done: data/v5/train.jsonl, data/v5/val.jsonl, data/v5/stats.md =="
