import argparse
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

from config import PipelineConfig
from logger import get_logger
from validations import run_validations
from pii_masking import apply_pii_masking
from transformations import add_derived_fields, select_output_columns
from utils import print_quick_stats

logger = get_logger("pipeline")

def build_spark(app_name: str = "secure-transaction-pipeline") -> SparkSession:
    return (
        SparkSession.builder
        .appName(app_name)
        .getOrCreate()
    )

def read_input(spark: SparkSession, path: str):
    logger.info(f"Reading input CSV: {path}")
    df = (
        spark.read
        .option("header", "true")
        .option("inferSchema", "true")
        .csv(path)
    )
    df = df.withColumn("txn_ts", F.to_timestamp(F.col("txn_ts")))
    return df

def write_output(df, out_path: str):
    logger.info(f"Writing output Parquet: {out_path}")
    (
        df.write
        .mode("overwrite")
        .partitionBy("txn_date")
        .parquet(out_path)
    )

def run(cfg: PipelineConfig, debug: bool = False):
    spark = build_spark()
    spark.conf.set("spark.sql.shuffle.partitions", str(cfg.shuffle_partitions))

    df = read_input(spark, cfg.input_path)
    if debug:
        logger.info('DEBUG: printing schema')
        df.printSchema()
        print_quick_stats(df, 'input')
    logger.info(f"Input rows: {df.count()}")

    df = run_validations(df)
    if debug:
        print_quick_stats(df, 'after_validations')
    logger.info(f"Rows after validations: {df.count()}")

    df = apply_pii_masking(df)
    df = add_derived_fields(df)
    df = select_output_columns(df)

    write_output(df, cfg.output_path)
    logger.info("Pipeline completed successfully")

    spark.stop()

def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--input", required=True, help="Input CSV path")
    p.add_argument("--output", required=True, help="Output Parquet path")
    p.add_argument("--debug", action="store_true", help="Enable extra prints for local runs")
    return p.parse_args()

if __name__ == "__main__":
    args = parse_args()
    cfg = PipelineConfig(input_path=args.input, output_path=args.output)
    run(cfg, debug=args.debug)
