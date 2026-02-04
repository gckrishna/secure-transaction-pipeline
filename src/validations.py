from pyspark.sql import functions as F

MANDATORY_COLS = ["txn_id", "customer_id", "product", "amount", "state", "txn_ts"]

def validate_columns(df, required_cols=MANDATORY_COLS):
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    return df

def validate_not_null(df, cols=("txn_id", "customer_id", "product", "txn_ts")):
    cond = None
    for c in cols:
        cnd = F.col(c).isNotNull()
        cond = cnd if cond is None else (cond & cnd)
    return df.filter(cond)

def validate_amount_positive(df, amount_col="amount"):
    return df.filter(F.col(amount_col) > 0)

def run_validations(df):
    df = validate_columns(df)
    df = validate_not_null(df)
    df = validate_amount_positive(df)
    return df
