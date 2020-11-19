import logging
import sys

from clients.postgress import PostgresClient

from utils import execute_elastic_query, get_courses_from_query, order_recommended_skills

from services.cluster_data_service import RecommenderService

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def find_matching_score_for_courses(courses_list):
    max_hits = find_max_hits(courses_list)
    for c in courses_list:
        hits = c['hits']
        c['score'] = hits / max_hits
        del c['hits']
    return courses_list


def find_max_hits(courses_list):
    max_hits = 0
    for c in courses_list:
        hits = c['hits']
        if hits > max_hits:
            max_hits = hits
    return max_hits


class Recommendation(object):
    """This Python Object implements Recommendation Pipeline"""

    def __init__(self):
        self.pg_client = PostgresClient()

    def find_related_jobs(self, **kwargs):
        """
        This function is used to find related jobs according to provided skills

        :param kwargs: provided kwargs
        :return: related job names
        """
        cv_skills = kwargs['cv_skills']

        lower_skills = [str(skill).lower() for skill in cv_skills]
        cv_skills_tuple = tuple(lower_skills)

        if len(cv_skills_tuple) == 1:
            sql_command = """SELECT * FROM extracted_skill WHERE lower(skill)='{}'""".format(cv_skills_tuple[0])
        else:
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
        important_jobs_string = [str(j) for j in important_jobs]
        return important_jobs_string

    def proposed_skills(self, important_jobs, initial_skills):
        """This function is used to find proposed skills per job name"""

        statement = """SELECT * FROM extracted_skill WHERE job_name in {}""".format(tuple(important_jobs))
        table_df = self.pg_client.get_table(sql_command=statement)

        initial_jobs_skills = table_df.loc[table_df['skill'].isin(initial_skills)]

        table_df = table_df.loc[~table_df['skill'].isin(initial_skills)]

        proposed_skills_per_job = self.get_top_skills(job_skills=table_df, column='job_name', topN=5).reset_index(
            drop=True)
        return proposed_skills_per_job, initial_jobs_skills

    def elk_recommend(self, **kwargs):
        """This function is used to find proper recommendations for provided skills"""

        cv_skills = kwargs['cv_skills']

        top_job_skills = self.find_related_jobs(cv_skills=cv_skills)
        get_top_jobs = self.get_top_skills(top_job_skills, column='skill', topN=3)

        important_jobs = self.find_unique_jobs(get_top_jobs)
        get_proposed_skills, initial_jobs_skills = self.proposed_skills(important_jobs, cv_skills)

        courses_list = []
        skills_list = []

        for job in important_jobs:
            job_top_skills, skills_list = self.extract_job_top_skills(get_proposed_skills,
                                                                      initial_jobs_skills,
                                                                      job,
                                                                      skills_list
                                                                      )
            self.extract_recommended_courses(courses_list, job_top_skills)

        unique_recommended_skills = order_recommended_skills(skills_list)
        unique_recommended_courses = courses_list

        log.info(unique_recommended_skills)
        log.info(unique_recommended_courses)
        return {"recommended_skills": order_recommended_skills(skills_list),
                "recommended_courses": courses_list}

    def recommend(self, **kwargs):
        """This function is used to find proper recommendations for provided skills"""

        cv_skills = kwargs['cv_skills']
        courses_list = []

        if len(cv_skills) > 0:
            str_skills = [str(skill) for skill in cv_skills]
            clustering_recommended_skills = self.get_clustering_recommended_skills(str_skills)

            top_job_skills = self.find_related_jobs(cv_skills=cv_skills)
            get_top_jobs = self.get_top_skills(top_job_skills, column='skill', topN=3)

            important_jobs = self.find_unique_jobs(get_top_jobs)
            get_proposed_skills, initial_jobs_skills = self.proposed_skills(important_jobs, cv_skills)

            skills_list = clustering_recommended_skills
            self.extract_recommended_courses(courses_list, clustering_recommended_skills)

            for job in important_jobs:
                job_top_skills, skills_list = self.extract_job_top_skills(get_proposed_skills,
                                                                          initial_jobs_skills,
                                                                          job,
                                                                          skills_list
                                                                          )
                self.extract_recommended_courses(courses_list, job_top_skills)

            unique_recommended_skills = order_recommended_skills(skills_list)
            unique_recommended_courses = courses_list

            log.info(unique_recommended_skills)
            log.info(unique_recommended_courses)
            final_skills = order_recommended_skills(skills_list)
        else:
            final_skills = self.find_top_skills()
            self.extract_recommended_courses(courses_list, final_skills)
        find_matching_score_for_courses(courses_list)

        return {"recommended_skills": final_skills,
                "recommended_courses": courses_list}

    @staticmethod
    def get_clustering_recommended_skills(cv_skills):
        recommender_service = RecommenderService(cv_skills)
        clustering_recommended_skills = recommender_service.get_recommended_skills()

        skills = [str(s) for key in clustering_recommended_skills for s in clustering_recommended_skills[key]]
        unique_skills = set(skills)
        return list(unique_skills)

    @staticmethod
    def extract_recommended_courses(courses_list, job_top_skills):
        """
        Iteratively completes recommended courses list
        :param courses_list: existing courses list
        :param job_top_skills: batch of top skills for given job title
        :return:
        """
        query_response = execute_elastic_query(job_top_skills)
        courses_from_batch = get_courses_from_query(query_response)
        print('__________courses_from_batch = ', query_response)

        for element in courses_from_batch:
            if element not in courses_list:
                courses_list.append(element)

    @staticmethod
    def extract_job_top_skills(get_proposed_skills, initial_jobs_skills, job, skills_list):
        """This function returns a list of skills regarding the given batch and a contineuously updated list of
        recommended skills  """
        log.info("Job: {}".format(job))

        init_job_part = initial_jobs_skills.loc[initial_jobs_skills['job_name'] == job]
        init_job_top_skills = init_job_part['skill'].to_list()

        job_part = get_proposed_skills.loc[get_proposed_skills['job_name'] == job]
        recommended_top_skills = job_part['skill'].to_list()

        skills_list = skills_list + recommended_top_skills
        job_top_skills = init_job_top_skills + recommended_top_skills
        return job_top_skills, skills_list

    def find_top_skills(self, skills_count=20):
        """
        This function is used to find the top required skills

        :return: skill names
        """
        sql_command = """SELECT * FROM extracted_skill where kind='tool' order by 4 desc limit {}""".format(
            skills_count)
        top_skills = self.pg_client.get_table(sql_command=sql_command)
        skills_list = [rows.skill for _, rows in top_skills.iterrows()]
        return skills_list
