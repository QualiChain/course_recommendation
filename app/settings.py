import os

# PostgreSQL Settings
POSTGRES_USER = os.environ.get("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "api_db")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "qualichain.epu.ntua.gr")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)

ENGINE_STRING = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_DB
)

QUALICHAIN_ENGINE_STRING = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    'admin',
    'admin',
    os.environ.get('QUALICHAIN_DB_HOST', 'qualichain.epu.ntua.gr'),
    os.environ.get('QUALICHAIN_DB_PORT', 5435),
    'qualichain_db'
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

# APP SETTINGS
API_PORT = os.environ.get('API_PORT', 7000)

