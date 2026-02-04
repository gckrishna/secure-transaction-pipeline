from pyspark.sql import functions as F
from pyspark.sql.types import StringType

def mask_card_py(card: str) -> str | None:
    if card is None:
        return None
    s = str(card).strip()
    if len(s) < 4:
        return None
    return "XXXX-XXXX-XXXX-" + s[-4:]

def mask_email_py(email: str) -> str | None:
    if email is None:
        return None
    s = str(email).strip()
    if "@" not in s:
        return None
    name, domain = s.split("@", 1)
    if not name:
        return "***@" + domain
    return name[0] + "***@" + domain

_mask_card_udf = F.udf(mask_card_py, StringType())
_mask_email_udf = F.udf(mask_email_py, StringType())

def apply_pii_masking(df, card_col: str = "card_number", email_col: str = "email"):
    return (
        df
        .withColumn(card_col, _mask_card_udf(F.col(card_col)))
        .withColumn(email_col, _mask_email_udf(F.col(email_col)))
    )
