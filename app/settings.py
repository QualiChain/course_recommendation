import os

# PostgreSQL Settings
POSTGRES_USER = os.environ.get("POSTGRES_USER", "")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "")

ENGINE_STRING = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_DB
)

# Analeyezer Settings
ANALEYEZER_HOST = os.environ.get("ANALEYEZER_HOST", "")
ANALEYEZER_PORT = os.environ.get("ANALEYEZER_PORT", 0)

ASK_STORAGE_URI = "http://{}:{}/ask/storage".format(
    ANALEYEZER_HOST,
    ANALEYEZER_PORT
)
SUBMIT_SOURCE = "http://{}:{}/receive/source".format(
    ANALEYEZER_HOST,
    ANALEYEZER_PORT
)

# APP SETTINGS
API_PORT = os.environ.get('API_PORT', 1)

