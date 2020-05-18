from app.clients.postgress import PostgresClient


class Recommendation(object):
    """This Python Object implements Recommendation Pipeline"""

    def find_related_jobs(self, **kwargs):
        """
        This function is used to find related jobs according to provided skills

        :param kwargs:
        :return:
        """


sql_command = """SELECT * FROM extracted_skill WHERE skill in ('Java', 'SQL')"""

pg_client = PostgresClient()
table_df = pg_client.get_table(sql_command=sql_command)
print(table_df.head())

top3 = table_df.groupby(['skill']).apply(lambda x: x.nlargest(3,['frequencyOfMention'])).reset_index(drop=True)
