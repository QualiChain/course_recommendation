from services.recommendation import Recommendation

r = Recommendation()
top_job_skills = r.find_related_jobs(cv_skills=['Java', 'SQL'])
top3 = top_job_skills.groupby(['skill']).apply(lambda x: x.nlargest(3, ['frequencyOfMention'])).reset_index(drop=True)
important_jobs = top3.groupby('job_name').sum().sort_values('frequencyOfMention', ascending=False).reset_index()['job_name'].to_list()

statement = """SELECT * FROM extracted_skill WHERE job_name in {}""".format(tuple(important_jobs))
table_df = r.pg_client.get_table(sql_command=statement)
sp = table_df.groupby('job_name').apply(lambda x: x.nlargest(5, ['frequencyOfMention'])).reset_index(drop=True)
print(sp)