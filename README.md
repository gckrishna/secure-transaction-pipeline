# secure-transaction-pipeline (PySpark)

Small PySpark batch pipeline I built as a side project to practice "banking-ish" ETL patterns:
- basic validations
- PII masking (card/email)
- simple derived fields
- parquet output (partitioned)

This is intentionally not a huge framework. It's a practical demo of how I'd structure a small pipeline.

## Quick run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
bash run_pipeline.sh
```

Input: `data/raw/transactions.csv`  
Output: `data/masked/output_parquet/`

## TODO / next ideas
- add a small Airflow DAG (maybe later)
- add schema drift check (columns added/removed)
- better error handling + metrics
