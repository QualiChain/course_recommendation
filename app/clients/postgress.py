from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import pandas as pd

from settings import ENGINE_URI


class PostgresClient(object):
    """
    This is a Python Object that handles Postgress DB using SQLAlchemy
    """

    def __init__(self):
        self.engine = create_engine(ENGINE_URI)

    def get_table(self, table, sql_command=None):
        """
        This function is used to load the provided table as a Pandas DataFrame

        :param table: provided table name
        :param sql_command: provided sql command to filter table
        :return: pandas DataFrame
        """
        if sql_command:
            table_df = pd.read_sql_query(sql_command, self.command)
        else:
            table_df = pd.read_sql_table(table, self.engine)

        return table_df

    def load_tables(self):
        """This function is used to load these tables"""

        courses_df = pd.read_sql_table('curriculum_designer_course', self.engine)
        course_skill_df = pd.read_sql_table('curriculum_designer_course_course_skills', self.engine)
        skill_df = pd.read_sql_table('curriculum_designer_skill', self.engine)
        return courses_df, course_skill_df, skill_df

    def join_skills_and_courses(self):
        """This function is used to join courses and skills tables"""

        print("Joining tables Skills and Courses")
        courses_df, course_skill_df, skill_df = self.load_tables()
        temp = pd.merge(courses_df, course_skill_df, left_on='id', right_on='course_id')
        joined_table = pd.merge(temp, skill_df, left_on='skill_id', right_on='id')
        joined_table = joined_table[['id', 'course_title', 'course_description', 'skill_id', 'skill_title']].rename(
            columns={'id': 'course_id'})
        return joined_table

    def load_joined_table_to_db(self):
        """Upload joined table to DB"""

        print("Uploading joined table to Postgres")
        joined_table = self.join_skills_and_courses()
        joined_table.to_sql('skills_courses_table', con=self.engine)
