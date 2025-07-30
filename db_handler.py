"""
Light-weight PostgreSQL helper for Neon
--------------------------------------

Usage examples
--------------

# 1) Run a simple test query
python db-handler.py

# 2) Import in another module
from db_handler import execute_query, execute_many

rows = execute_query("SELECT * FROM tree_data WHERE id < %s;", (10,), fetch=True)
print(rows)

# 3) Use as a context manager for custom work
from db_handler import get_connection
with get_connection() as conn:
    with conn.cursor() as cur:
        cur.execute("VACUUM;")
"""
import os
import sys
from contextlib import contextmanager
from typing import Any, Iterable, List, Optional

import psycopg2                            # pip install psycopg2-binary
from psycopg2.extras import RealDictCursor

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
    Yields a psycopg2 connection with sslmode=require.
    Automatically closes the connection when the block exits.
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

    Args:
        query   – SQL string with %s placeholders.
        params  – tuple/list/dict of parameters.
        fetch   – if True, returns fetched rows (list of dicts).

    Returns:
        list[dict] if fetch is True; otherwise None.
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
    Run the same SQL statement on many sets of parameters (bulk insert/update).
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            psycopg2.extras.execute_batch(cur, query, seq_of_params)
        conn.commit()


# ---------------------------------------------------------------------
# Simple CLI test
# ---------------------------------------------------------------------
if __name__ == "__main__":
    try:
        result = execute_query("SELECT current_database();", fetch=True)
        print("✅ Connected! Current database:", result[0]["current_database"])
    except Exception as exc:  # noqa: BLE001
        print("❌ Connection failed:", exc, file=sys.stderr)
        sys.exit(1)
