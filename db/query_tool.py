from typing import List, Dict
from psycopg2.extras import RealDictCursor
from db.connection import get_connection

def query_company_db(sql: str) -> List[Dict]:
    """
    Run a read-only SELECT against the company schema and return list of dict rows.
    This function validates the SQL superficially and only creates a DB connection
    when actually called.
    """
    if not sql or not sql.strip():
        raise ValueError("SQL must be provided.")
    sql_stripped = sql.strip()
    if not sql_stripped.upper().startswith("SELECT"):
        raise ValueError("Only SELECT statements are allowed for read-only access.")
    if "company." not in sql_stripped.lower():
        raise ValueError("Only queries on the 'company' schema are permitted.")

    # Use RealDictCursor to get column-name -> value mappings
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql)
            return cur.fetchall()
