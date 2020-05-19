from services.recommendation import Recommendation

r = Recommendation()
top_job_skills = r.find_related_jobs(cv_skills=['Java', 'SQL'])
top3 = top_job_skills.groupby(['skill']).apply(lambda x: x.nlargest(3, ['frequencyOfMention'])).reset_index(drop=True)
print(top3.groupby('job_name').sum().sort_values('frequencyOfMention', ascending=False).reset_index()['job_name'].to_list())