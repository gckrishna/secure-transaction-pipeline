from pyspark.sql import DataFrame

def print_quick_stats(df: DataFrame, label: str = "df"):
    print(f"--- {label} ---")
    print("cols:", len(df.columns))
    #TO Check and change - count() triggers action;
    print("rows:", df.count())
