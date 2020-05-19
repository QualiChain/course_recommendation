from clients.postgress import PostgresClient


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

        lower_skills = [skill.lower() for skill in cv_skills]
        cv_skills_tuple = tuple(lower_skills)

        sql_command = """SELECT * FROM extracted_skill WHERE lower(skill) in {}""".format(cv_skills_tuple)
        top_job_skills = self.pg_client.get_table(sql_command=sql_command)
        return top_job_skills

    @staticmethod
    def get_top_skills(job_skills, topN=3):
        """
        This function is used to retrieve top skills for job names

        :param job_skills: job_skills pandas DataFrame
        :param topN: topN skills for each job name,default=3
        :return: top skills
        """
        top_skills = job_skills.groupby(['skill']).apply(
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



# sql_command = """SELECT * FROM extracted_skill WHERE skill in ('Java', 'SQL')"""
#
# pg_client = PostgresClient()
# table_df = pg_client.get_table(sql_command=sql_command)
# print(table_df.head())
#
# top3 = table_df.groupby(['skill']).apply(lambda x: x.nlargest(3, ['frequencyOfMention'])).reset_index(drop=True)
