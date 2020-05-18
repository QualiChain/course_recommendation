from app.clients.postgress import PostgresClient


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
        top_job_skills = pg_client.get_table(sql_command=sql_command)


sql_command = """SELECT * FROM extracted_skill WHERE skill in ('Java', 'SQL')"""

pg_client = PostgresClient()
table_df = pg_client.get_table(sql_command=sql_command)
print(table_df.head())

top3 = table_df.groupby(['skill']).apply(lambda x: x.nlargest(3, ['frequencyOfMention'])).reset_index(drop=True)
