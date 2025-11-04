import os
import psycopg2

def get_connection():
    """
    Return a psycopg2 connection.

    Priority:
      1) Use DATABASE_URL if set (Heroku Postgres or remote DSN).
      2) Otherwise use DB_HOST/DB_PORT/DB_NAME/DB_USER/DB_PASSWORD env vars.
    Raises RuntimeError with a clear message if configuration is missing.
    """
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        # Many managed DBs require SSL; default to require unless overridden.
        sslmode = os.getenv("DB_SSLMODE", "require")
        return psycopg2.connect(database_url, sslmode=sslmode)

    # Fallback to explicit DB_* environment variables (useful for local dev)
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT", "5432")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    sslmode = os.getenv("DB_SSLMODE", "require")

    missing = [k for k, v in (
        ("DB_HOST", host),
        ("DB_NAME", dbname),
        ("DB_USER", user),
        ("DB_PASSWORD", password),
    ) if not v]
    if missing:
        raise RuntimeError(
            "Missing required database environment variables: " + ", ".join(missing)
            + ". Set DATABASE_URL or the DB_* config vars in Heroku (Settings → Config Vars)."
        )

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        sslmode=sslmode,
    )
