"""
db_handler.py
-------------
Light-weight PostgreSQL helper for Neon.

Features
--------
• Environment-driven DATABASE_URL (falls back to DEFAULT_DB_URL).
• Context-manager connection to ensure close().
• execute_query()  – run one statement, fetch optional.
• execute_many()   – bulk insert/update.
• Command-line utilities:
    └─ python db_handler.py               # quick connection test
    └─ python db_handler.py --cleanup-duplicates
       (deletes duplicate trees + adds UNIQUE constraint)
"""

import os
import sys
from contextlib import contextmanager
from typing import Any, Iterable, List, Optional

import psycopg2                      # pip install psycopg2-binary
from psycopg2.extras import RealDictCursor, execute_batch

# ---------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------
DEFAULT_DB_URL = (
    "postgresql://neondb_owner:"
    "npg_qBfRYC3K8FHx@ep-icy-queen-a2xo0tqj-pooler.eu-central-1.aws.neon.tech/"
    "neondb?sslmode=require&channel_binding=require"
)

DATABASE_URL: str = os.getenv("DATABASE_URL", DEFAULT_DB_URL)

# ---------------------------------------------------------------------
# Connection helper
# ---------------------------------------------------------------------
@contextmanager
def get_connection():
    """
    Yields a psycopg2 connection. Closes it automatically on exit.
    """
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()

# ---------------------------------------------------------------------
# Query helpers
# ---------------------------------------------------------------------
def execute_query(
    query: str,
    params: Optional[tuple | list | dict] = None,
    *,
    fetch: bool = False,
) -> List[Any] | None:
    """
    Run a single SQL statement.
    If fetch=True, returns list[dict]; else returns None.
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, params)
            if fetch:
                result = cur.fetchall()
            conn.commit()
    return result if fetch else None


def execute_many(query: str, seq_of_params: Iterable[tuple | list | dict]):
    """
    Bulk insert/update – wraps psycopg2.extras.execute_batch().
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_batch(cur, query, seq_of_params)
        conn.commit()

# ---------------------------------------------------------------------
# CLI utilities
# ---------------------------------------------------------------------
# ---------------------------------------------------------------------
# CLI utilities (connection test or duplicate cleanup)
# ---------------------------------------------------------------------
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="DB helper CLI")
    parser.add_argument(
        "--cleanup-duplicates",
        action="store_true",
        help="Remove duplicate tree rows and add UNIQUE constraint",
    )
    args = parser.parse_args()

    if args.cleanup_duplicates:
        print("🔄  Cleaning duplicates in tree_data…")

        # 1) Delete duplicates (keep the first ID)
        execute_query(
            """
            BEGIN;
            WITH ranked AS (
              SELECT id,
                     ROW_NUMBER() OVER (
                       PARTITION BY tree_name, scientific_name
                       ORDER BY id
                     ) AS rn
              FROM tree_data
            )
            DELETE FROM tree_data
            USING ranked
            WHERE tree_data.id = ranked.id
              AND ranked.rn > 1;
            COMMIT;
            """
        )

        # 2) Add UNIQUE constraint only if it doesn't already exist
        execute_query(
            """
            DO $$
            BEGIN
              IF NOT EXISTS (
                SELECT 1
                FROM   pg_constraint
                WHERE  conname = 'tree_unique_name_scientific'
              ) THEN
                ALTER TABLE tree_data
                ADD CONSTRAINT tree_unique_name_scientific
                  UNIQUE (tree_name, scientific_name);
              END IF;
            END
            $$;
            """
        )

        print("✅  Done! Duplicates removed and UNIQUE constraint added.")

    else:
        # Default: simple connectivity test
        result = execute_query("SELECT current_database();", fetch=True)
        print("Connected to:", result[0]["current_database"])
