import os

POSTGRES_USER = os.environ.get("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "api_db")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "qualichain.epu.ntua.gr")
