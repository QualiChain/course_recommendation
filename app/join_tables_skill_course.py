
from clients.postgress import *

from utils import create_joined_table_index

if __name__ == "__main__":
    post_client = PostgresClient()
    post_client.load_joined_table_to_db()

    create_joined_table_index()