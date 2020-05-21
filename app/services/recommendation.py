import logging
import sys

from clients.postgress import PostgresClient
from clients.analeyezer import AnalEyeZerClient

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


class Recommendation(object):
    """This Python Object implements Recommendation Pipeline"""

    def __init__(self):
        self.pg_client = PostgresClient()

    # def start_recommendation(self):
    #     if self.source_type == 'cv':
    #         if self.recommendation_type == 'courses':
    #             skills_list = self.retrieve_skills_from_cv()
    #             elastic_query = self.create_elastic_query_for_courses(skills_list)
    #             query_response = ask_analeyezer(elastic_query)
    #         elif self.recommendation_type == 'skills':
    #             pass
    #         elif self.recommendation_type == 'job_titles':
    #             pass
    #     elif self.source_type == 'skills':
    #         if self.recommendation_type == 'courses':
    #             pass
    #         elif self.recommendation_type == 'skills':
    #             pass
    #         elif self.recommendation_type == 'job_titles':
    #             pass
    #     elif self.source_type == 'job_titles':
    #         if self.recommendation_type == 'courses':
    #             pass
    #         elif self.recommendation_type == 'skills':
    #             pass

    def find_related_jobs(self, **kwargs):
        """
        This function is used to find related jobs according to provided skills

        :param kwargs: provided kwargs
        :return: related job names
        """
        cv_skills = kwargs['cv_skills']

        lower_skills = [skill.lower() for skill in cv_skills]
        cv_skills_tuple = tuple(lower_skills)

        sql_command = """SELECT * FROM extracted_skill WHERE lower(skill) in {}""".format(cv_skills_tuple)
        top_job_skills = self.pg_client.get_table(sql_command=sql_command)
        return top_job_skills

    @staticmethod
    def get_top_skills(job_skills, column, topN=3):
        """
        This function is used to retrieve top skills for job names

        :param job_skills: job_skills pandas DataFrame
        :param column: this column could be `skill` or `job_name`
        :param topN: topN skills for each job name,default=3
        :return: top skills
        """
        top_skills = job_skills.groupby([column]).apply(
            lambda grp: grp.nlargest(topN, ['frequencyOfMention']).reset_index(drop=True)
        )
        return top_skills

    @staticmethod
    def find_unique_jobs(top_skills):
        """
        This function is used to find most important job names from skills provided

        :param top_skills: job skills pandas DataFrame
        :return: important jobs in descending order of importance
        """
        jobs = top_skills.groupby('job_name').sum().sort_values('frequencyOfMention', ascending=False).reset_index()
        important_jobs = jobs['job_name'].to_list()
        return important_jobs

    def proposed_skills(self, important_jobs, initial_skills):
        """This function is used to find proposed skills per job name"""

        statement = """SELECT * FROM extracted_skill WHERE job_name in {}""".format(tuple(important_jobs))
        table_df = self.pg_client.get_table(sql_command=statement)

        initial_jobs_skills = table_df.loc[table_df['skill'].isin(initial_skills)]

        table_df = table_df.loc[~table_df['skill'].isin(initial_skills)]

        proposed_skills_per_job = self.get_top_skills(job_skills=table_df, column='job_name', topN=5).reset_index(
            drop=True)
        return proposed_skills_per_job, initial_jobs_skills

    def recommend(self, **kwargs):
        """This function is used to find proper recommendations for provided skills"""

        cv_skills = kwargs['cv_skills']

        top_job_skills = self.find_related_jobs(cv_skills=cv_skills)
        get_top_jobs = self.get_top_skills(top_job_skills, column='skill', topN=3)

        importan_jobs = self.find_unique_jobs(get_top_jobs)
        get_proposed_skills, initial_jobs_skills = self.proposed_skills(importan_jobs)
        courses_list = []
        for job in importan_jobs:
            query_response = self.execute_elastic_query(job, get_proposed_skills)
            courses_from_batch = self.get_courses_from_query(query_response)
            courses_list.append(courses_from_batch)
            init_job_part = initial_jobs_skills.loc[initial_jobs_skills['job_name'] == job]
            init_job_top_skills = init_job_part['skill'].to_list()

            job_part = get_proposed_skills.loc[get_proposed_skills['job_name'] == job]
            recommended_top_skills = job_part['skill'].to_list()

            job_top_skills = init_job_top_skills + recommended_top_skills

            log.info(job_top_skills)
        print(courses_list)


    def execute_elastic_query(self, job, proposed_skills):
        log.info("Job: {}".format(job))
        job_part = proposed_skills.loc[proposed_skills['job_name'] == job]
        job_top_skills = job_part['skill'].to_list()
        analeyezer_client = AnalEyeZerClient()
        query = analeyezer_client.create_elastic_query_for_courses(job_top_skills)
        query_response = analeyezer_client.ask_analeyezer(query=query)
        return query_response

    def get_courses_from_query(self, query_response):
        course_list =[]
        for course in query_response.json()['top_tags']['buckets']:
            element = course['top_course_hits']['hits']['hits'][0]['_source']
            course_list.append((element['course_title'], element['course_id']))
        return course_list