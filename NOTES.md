# Notes

Random notes while building this:

- kept masking logic in Python UDFs for simplicity.
  In real projects I'd try to avoid UDFs and use native functions where possible.

- Current validations are basic (nulls, amount > 0). Could add:
  - duplicate txn_id checks
  - allowed states list
  - range checks (amount upper bound)

- If running on a real cluster:
  - tune shuffle partitions
  - think about skewed keys
