import logging
import sys

from sqlalchemy import create_engine
import pandas as pd
import numpy as np

from settings import ENGINE_STRING, QUALICHAIN_ENGINE_STRING

from utils import filter_extracted_skills, remove_dump_skills

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class PostgresClient(object):
    """
    This is a Python Object that handles Postgress DB using SQLAlchemy
    """

    def __init__(self):
        self.engine = create_engine(ENGINE_STRING)
        self.qualichain_db_engine = create_engine(QUALICHAIN_ENGINE_STRING)

    def match_saro_skills(self, skills):
        """This function is used to match skills from Qualichain DB"""
        transformed_skills = [skill.lower() for skill in skills]
        GET_SKILLS = """SELECT id, name FROM skills WHERE lower(name) in {skills}""".format(
            skills=tuple(transformed_skills)
        )
        skills_data = pd.read_sql_query(GET_SKILLS, self.qualichain_db_engine)

        skills_data['name'] = skills_data['name'].apply(lambda x: x.lower())
        skills_data = skills_data.drop_duplicates(subset=['name'])

        skills_info = list(skills_data.to_dict(orient='index').values())
        skills_info_sorted = sorted(skills_info, key=lambda x: transformed_skills.index(x['name'].lower()))
        return skills_info_sorted

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
        data_frame.to_sql(table_name, if_exists=if_exists, con=self.engine, index=False)

    def load_tables(self):
        """This function is used to load these tables"""

        courses_df = pd.read_sql_table('curriculum_designer_course', self.engine)
        course_skill_df = pd.read_sql_table('curriculum_designer_course_course_skills', self.engine)
        skill_df = pd.read_sql_table('curriculum_designer_skill', self.engine)
        return courses_df, course_skill_df, skill_df

    def join_skills_and_courses(self):
        """This function is used to join courses and skills tables"""

        log.info("Joining tables Skills and Courses")
        courses_df, course_skill_df, skill_df = self.load_tables()

        temp = pd.merge(courses_df, course_skill_df, left_on='id', right_on='course_id')
        joined_table = pd.merge(temp, skill_df, left_on='skill_id', right_on='id')

        joined_table = joined_table[['id_x', 'course_title', 'course_description', 'skill_id', 'skill_title']].rename(
            columns={'id_x': 'course_id'})
        grouped_courses_skills = joined_table.groupby('course_id').agg({
            'skill_id': lambda x: list(x),
            'skill_title': lambda x: list(x)}
        ).reset_index()
        joined_courses_info = pd.merge(grouped_courses_skills, courses_df, left_on='course_id', right_on='id')[
            ['course_id', 'course_name', 'course_title', 'course_description', 'skill_id', 'skill_title']
        ]
        return joined_courses_info

    def handle_qualichain_courses_data(self):
        """This function is used to load and handle QualiChain courses skills relation from Dobie"""
        qc_courses_skills = pd.read_sql_table('skills_courses', self.qualichain_db_engine)
        qc_skills = pd.read_sql_table('skills', self.qualichain_db_engine)

        qc_merged_info = pd.merge(qc_courses_skills, qc_skills, left_on='skill_id', right_on='id')
        grouped_qc_info = qc_merged_info.groupby('course_id').agg({
            'name': lambda x: list(x)
        }).reset_index().rename(columns={'name': 'dobie_skill_title'})
        return grouped_qc_info

    def construct_df_with_all_skills(self):
        """This function is used to combine ntua curriculum with skills extracted from Dobie"""
        ntua_curriculum_info = self.join_skills_and_courses()
        courses_skills_from_dobie = self.handle_qualichain_courses_data()

        merged_data = pd.merge(ntua_curriculum_info, courses_skills_from_dobie, how='outer', on='course_id')
        merged_data['dobie_skill_title'] = merged_data['dobie_skill_title'].apply(lambda x: [] if x is np.NaN else x)

        merged_data = merged_data[merged_data['course_name'].notna()]
        merged_data['skill_title'] = merged_data['skill_title'].apply(lambda x: ",".join(x))
        merged_data['dobie_skill_title'] = merged_data['dobie_skill_title'].apply(lambda x: ",".join(x))
        return merged_data

    def load_joined_table_to_db(self, skills_courses_info):
        """Upload joined table to DB"""

        log.info("Uploading joined table to Postgres")

        self.save_table(
            table_name='skills_courses_table',
            data_frame=skills_courses_info,
            if_exists='replace'
        )
        log.info("Table saved to Postgres")

    def transform_extracted_skills(self):
        """This function is used to transform skills in extracted skill"""
        table_name = 'extracted_skill'
        if_exists = 'replace'

        extracted_skills = self.get_table(table=table_name)
        extracted_skills['skill'] = extracted_skills['skill'].apply(lambda skill: filter_extracted_skills(skill=skill))
        extr_skills = remove_dump_skills(extracted_skills)

        self.save_table(
            table_name=table_name,
            data_frame=extr_skills,
            if_exists=if_exists
        )
