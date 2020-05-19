
from clients.postgress import PostgresClient

from utils import create_joined_table_index

if __name__ == "__main__":
    post_client = PostgresClient()

    uri = "postgresql://admin:admin@mediator_api_db:5432/api_db"
    type = "POSTGRES"
    part = "skills_courses_table"
    index = "curriculum_index"

    post_client.load_joined_table_to_db()

    create_joined_table_index(
        uri=uri,
        type=type,
        part=part,
        index=index
    )

    print("Transform saved extracted skills from Dobie", flush=True)
    post_client.transform_extracted_skills()