from pyspark.sql import functions as F

def add_derived_fields(df):
    # txn_date for partitioning
    df = df.withColumn("txn_date", F.to_date(F.col("txn_ts")))
    # simple amount bucket
    df = df.withColumn(
        "amount_bucket",
        F.when(F.col("amount") < 100, F.lit("LOW"))
         .when(F.col("amount") < 1000, F.lit("MED"))
         .otherwise(F.lit("HIGH"))
    )
    return df

def select_output_columns(df):
    cols = [
        "txn_id", "customer_id", "product",
        "card_number", "email",
        "amount", "amount_bucket",
        "state", "txn_ts", "txn_date"
    ]
    existing = [c for c in cols if c in df.columns]
    return df.select(*existing)
