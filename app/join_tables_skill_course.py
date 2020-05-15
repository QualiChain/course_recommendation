
from clients.postgress import *

if __name__ == "__main__":
    post_client = PostgresClient()
    post_client.initialize_tables()
    # post_client.create_joined_table_skills_courses()