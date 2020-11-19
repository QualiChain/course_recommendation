import logging
import sys

from clients.postgress import PostgresClient

from utils import create_joined_table_index

from settings import POSTGRES_USER, POSTGRES_HOST, POSTGRES_PORT, POSTGRES_DB,CURRICULUM_INDEX

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def skills_courses_to_index():
    """This function is used to upload skills courses information to AnaleyeZer"""
    post_client = PostgresClient()

    uri = "postgresql://{}:{}@{}:{}/{}".format(
        POSTGRES_USER,
        POSTGRES_USER,
        POSTGRES_HOST,
        POSTGRES_PORT,
        POSTGRES_DB
    )
    type = "POSTGRES"
    part = "skills_courses_table"
    index = CURRICULUM_INDEX

    table_exists = post_client.engine.has_table(part)
    if not table_exists:
        courses_skills_info = post_client.construct_df_with_all_skills()
        post_client.load_joined_table_to_db(courses_skills_info)
    else:
        log.info("Table: {} already exists -- Continue".format(part))

    create_joined_table_index(
        uri=uri,
        type=type,
        part=part,
        index=index
    )

    log.info("Transform saved extracted skills from Dobie")
    post_client.transform_extracted_skills()


if __name__ == "__main__":
    skills_courses_to_index()


