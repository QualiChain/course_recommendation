
from clients.postgress import *

if __name__ == "__main__":
    post_client = PostgresClient()
    post_client.load_joined_table_to_db()