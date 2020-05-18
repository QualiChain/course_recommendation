from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import pandas as pd

from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB


class PostgresClient(object):
    """
    This is a Python Object that handles Postgress DB using SQLAlchemy
    """

    def __init__(self):
        self.engine = create_engine(
            'postgresql+psycopg2://{}:{}@{}/{}'.format(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB)
        )

    def load_tables(self):
        courses_df = pd.read_sql_table('curriculum_designer_course', self.engine)
        course_skill_df = pd.read_sql_table('curriculum_designer_course_course_skills', self.engine)
        skill_df = pd.read_sql_table('curriculum_designer_skill', self.engine)
        return courses_df, course_skill_df, skill_df

    def join_skills_and_courses(self):
        print("Joining tables Skills and Courses")
        courses_df, course_skill_df, skill_df = self.load_tables()
        temp = pd.merge(courses_df, course_skill_df, left_on='id', right_on='course_id')
        joined_table = pd.merge(temp, skill_df, left_on='skill_id', right_on='id')
        joined_table = joined_table[['id', 'course_title', 'course_description', 'skill_id', 'skill_title']].rename(
            columns={'id': 'course_id'})
        return joined_table

    def load_joined_table_to_db(self):
        print("Uploading joined table to Postgres")
        joined_table = self.join_skills_and_courses()
        joined_table.to_sql('skills_courses_table', con=self.engine)
