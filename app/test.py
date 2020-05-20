from services.recommendation import Recommendation

r = Recommendation()
top_job_skills = r.find_related_jobs(cv_skills=['Java', 'SQL'])
get_top_jobs = r.get_top_skills(top_job_skills, column='skill', topN=3)
importan_jobs = r.find_unique_jobs(get_top_jobs)

print("These jobs are in descending order")
print(importan_jobs)
get_proposed_skills = r.proposed_skills(importan_jobs)
print(get_proposed_skills)
# statement = """SELECT * FROM extracted_skill WHERE job_name in {}""".format(tuple(important_jobs))
# table_df = r.pg_client.get_table(sql_command=statement)
# sp = table_df.groupby('job_name').apply(lambda x: x.nlargest(5, ['frequencyOfMention'])).reset_index(drop=True)
# print(sp)
