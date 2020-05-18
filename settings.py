import os


POSTGRES_USER = os.environ.get('POSTGRES_USER', 'admin')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'admin')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'qualichain.epu.ntua.gr')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT', 5432)
POSTGRES_DB = os.environ.get('POSTGRES_DB', 'api_db')


ENGINE_STRING = 'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(
    POSTGRES_USER,
    POSTGRES_PASSWORD,
    POSTGRES_HOST,
    POSTGRES_PORT,
    POSTGRES_DB
)

JOB_POSTS_TABLE = 'job_post'
