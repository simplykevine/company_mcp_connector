import os
import psycopg2
from dotenv import load_dotenv

# Load .env in development if present; harmless in Heroku
load_dotenv()

def get_connection():
    """
    Create and return a new psycopg2 connection.

    This is intentionally lazy (only runs when called) so the app does not
    crash at import time if environment variables are not set in non-production.
    """
    host = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    dbname = os.getenv("DB_NAME")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    sslmode = os.getenv("DB_SSLMODE", "require")

    # If any required DB env var is missing, raise a clear error when a connection is attempted.
    missing = [k for k, v in (
        ("DB_HOST", host),
        ("DB_PORT", port),
        ("DB_NAME", dbname),
        ("DB_USER", user),
        ("DB_PASSWORD", password),
    ) if not v]
    if missing:
        raise RuntimeError(
            "Missing required database environment variables: " + ", ".join(missing)
            + ". Set these in Heroku Config Vars (Settings → Config Vars)."
        )

    return psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password,
        sslmode=sslmode,
    )
