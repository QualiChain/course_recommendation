from sqlalchemy import create_engine
import pandas as pd

from settings import ENGINE_STRING

from utils import filter_extracted_skills


class PostgresClient(object):
    """
    This is a Python Object that handles Postgress DB using SQLAlchemy
    """

    def __init__(self):
        self.engine = create_engine(ENGINE_STRING)

    def get_table(self, **kwargs):
        """
        This function is used to load the provided table as a Pandas DataFrame

        :param kwargs: provided kwargs
        :return: pandas DataFrame
        """
        if 'sql_command' in kwargs.keys():
            sql_command = kwargs['sql_command']
            table_df = pd.read_sql_query(sql_command, self.engine)
        elif 'table' in kwargs.keys():
            table = kwargs['table']
            table_df = pd.read_sql_table(table, self.engine)
        else:
            table_df = pd.DataFrame()
        return table_df

    def save_table(self, table_name, data_frame, if_exists='fail'):
        """This function is used to save a pandas DataFrame to Postgress"""
        data_frame.to_sql(table_name, if_exists=if_exists, con=self.engine)

    def load_tables(self):
        """This function is used to load these tables"""

        courses_df = pd.read_sql_table('curriculum_designer_course', self.engine)
        course_skill_df = pd.read_sql_table('curriculum_designer_course_course_skills', self.engine)
        skill_df = pd.read_sql_table('curriculum_designer_skill', self.engine)
        return courses_df, course_skill_df, skill_df

    def join_skills_and_courses(self):
        """This function is used to join courses and skills tables"""

        print("Joining tables Skills and Courses", flush=True)

        courses_df, course_skill_df, skill_df = self.load_tables()
        temp = pd.merge(courses_df, course_skill_df, left_on='id', right_on='course_id')
        joined_table = pd.merge(temp, skill_df, left_on='skill_id', right_on='id')
        joined_table = joined_table[['id', 'course_title', 'course_description', 'skill_id', 'skill_title']].rename(
            columns={'id': 'course_id'})
        return joined_table

    def load_joined_table_to_db(self):
        """Upload joined table to DB"""

        print("Uploading joined table to Postgres", flush=True)

        table_exists = self.engine.has_table('skills_courses_table')
        if not table_exists:
            joined_table = self.join_skills_and_courses()
            self.save_table(
                table_name='skills_courses_table',
                data_frame=joined_table,
                if_exists='replace'
            )

    def transform_extracted_skills(self):
        """This function is used to transform skills in extracted skill"""
        table_name = 'extracted_skill'
        if_exists = 'replace'

        extracted_skills = self.get_table(table=table_name)
        extracted_skills['skill'] = extracted_skills['skill'].apply(lambda skill: filter_extracted_skills(skill=skill))

        self.save_table(
            table_name=table_name,
            data_frame=extracted_skills,
            if_exists=if_exists
        )
