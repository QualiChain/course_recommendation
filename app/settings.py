import os

# PostgreSQL Settings
POSTGRES_USER = os.environ.get("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "api_db")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "qualichain.epu.ntua.gr")

ENGINE_URI = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_DB
)

# Analeyezer Settings
ANALEYEZER_HOST = os.environ.get("ANALEYEZER_HOST", "qualichain.epu.ntua.gr")
ANALEYEZER_PORT = os.environ.get("ANALEYEZER_PORT", 5002)

ASK_STORAGE_URI = "http://{}:{}/ask/storage".format(
    ANALEYEZER_HOST,
    ANALEYEZER_PORT
)
SUBMIT_SOURCE = "http://{}:{}/receive/source".format(
    ANALEYEZER_HOST,
    ANALEYEZER_PORT
)
