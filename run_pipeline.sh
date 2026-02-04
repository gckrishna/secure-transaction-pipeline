#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

INPUT="${ROOT_DIR}/data/raw/transactions.csv"
OUTPUT="${ROOT_DIR}/data/masked/output_parquet"

spark-submit \
  --master "local[*]" \
  --driver-memory 2g \
  --executor-memory 2g \
  "${ROOT_DIR}/src/pipeline.py" \
  --input "${INPUT}" \
  --output "${OUTPUT}"
