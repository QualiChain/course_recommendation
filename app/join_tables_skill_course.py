import logging
import sys

from clients.postgress import PostgresClient

from utils import create_joined_table_index

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

if __name__ == "__main__":
    post_client = PostgresClient()

    uri = "postgresql://admin:admin@mediator_api_db:5432/api_db"
    type = "POSTGRES"
    part = "skills_courses_table"
    index = "curriculum_index"

    ntua_curriculum_info = post_client.join_skills_and_courses()

    # post_client.load_joined_table_to_db()
    # print(joined_table.head())

    # create_joined_table_index(
    #     uri=uri,
    #     type=type,
    #     part=part,
    #     index=index
    # )
    #
    # log.info("Transform saved extracted skills from Dobie")
    # post_client.transform_extracted_skills()
