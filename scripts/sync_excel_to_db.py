"""
scripts/sync_excel_to_db.py
---------------------------
Reads data/tree_data.xlsx and upserts each row into Neon.
Usage:
    python scripts/sync_excel_to_db.py
"""

from pathlib import Path
import pandas as pd
from db_handler import execute_many, execute_query

EXCEL_PATH = Path(__file__).resolve().parent.parent / "data/tree_data.xlsx"

# Ensure UNIQUE constraint so duplicates can’t appear
execute_query(
    """
    DO $$
    BEGIN
      IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'tree_unique_name_scientific'
      ) THEN
        ALTER TABLE tree_data
        ADD CONSTRAINT tree_unique_name_scientific
          UNIQUE (tree_name, scientific_name);
      END IF;
    END $$;
    """
)

df = pd.read_excel(EXCEL_PATH)

# Trim whitespace
df["tree_name"] = df["tree_name"].astype(str).str.strip()
df["scientific_name"] = df["scientific_name"].astype(str).str.strip()

cols = list(df.columns)
placeholders = ", ".join(["%s"] * len(cols))
col_list = ", ".join(cols)

update_sets = ", ".join(
    f"{c}=EXCLUDED.{c}"
    for c in cols
    if c not in ("tree_name", "scientific_name")
)

sql = f"""
INSERT INTO tree_data ({col_list})
VALUES ({placeholders})
ON CONFLICT (tree_name, scientific_name)
DO UPDATE SET {update_sets};
"""

data_tuples = [tuple(r) for r in df.itertuples(index=False, name=None)]

print(f"⏫  Syncing {len(data_tuples)} rows from Excel to Neon …")
execute_many(sql, data_tuples)
print("✅  Done! Excel and database are now in sync.")
