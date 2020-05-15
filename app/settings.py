import os

# PostgreSQL Settings
POSTGRES_USER = os.environ.get("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "admin")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "api_db")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "qualichain.epu.ntua.gr")

# Analeyezer Settings
ANALEYEZER_HOST = os.environ.get("ANALEYEZER_HOST", "qualichain.epu.ntua.gr")
ANALEYEZER_PORT = os.environ.get("ANALEYEZER_PORT", 5002)
