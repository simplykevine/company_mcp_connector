from db.connection import get_connection

def query_company_db(sql: str) -> list[dict]:
    sql_upper = sql.strip().upper()

    if not sql_upper.startswith("SELECT"):
        raise ValueError("Only SELECT statements are allowed for read-only access.")
    if "company." not in sql.lower():
        raise ValueError("Only queries on the 'company' schema are permitted.")

    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(sql)
            columns = [desc[0] for desc in cur.description]
            rows = [dict(zip(columns, row)) for row in cur.fetchall()]
    return rows
