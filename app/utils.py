import logging
import sys
from collections import OrderedDict

from clients.analeyezer import AnalEyeZerClient

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def filter_extracted_skills(**kwargs):
    """
    This function is used to transform extracted skill table

    :param kwargs: provided kwargs
    :return: filtered skill
    """
    skill = kwargs['skill']
    skills_to_transform = ["Java Script", "Type Script", "Lab VIEW"]

    split_skill = skill.split(" ")
    bins_len = len(split_skill)

    if bins_len > 2 or bins_len == 1:
        filtered_skill = skill
    else:
        first_bin = split_skill[0]
        second_bin = split_skill[1]

        if len(second_bin) <= 3 or len(first_bin) <= 2:
            filtered_skill = "".join(split_skill)
        elif skill in skills_to_transform:
            transformed_skill = skill.split()
            filtered_skill = "".join(transformed_skill)
        elif skill == "OOP":
            filtered_skill = "Object-oriented programming"
        else:
            filtered_skill = skill

    return filtered_skill


def remove_dump_skills(skills_df):
    """This function is used to remove dump skills extracted from Dobie"""
    remove_skills = skills_df.loc[~skills_df['skill'].isin(
        ['Assurance', 'LeSS', 'Computer Science', 'Development', 'Programming', 'BDD', 'TDD', 'Developer',
         'Software Engineer'])]
    return remove_skills


def create_joined_table_index(**kwargs):
    """
    This function is used to load the joined data source to elasticsearch
    """
    analeyezer = AnalEyeZerClient()
    response = analeyezer.commit_data_source(**kwargs)
    if response.status_code == 400:
        log.info('Index creation to Elasticsearch failed.')
    else:
        log.info('Index successfully created')


def order_recommended_skills(skills_list):
    """This function is used to keep unique skills in order"""
    recommended_skills = list(OrderedDict.fromkeys(skills_list))
    return recommended_skills


def execute_elastic_query(job_top_skills):
    analeyezer_client = AnalEyeZerClient()
    query = analeyezer_client.create_elastic_query_for_courses(job_top_skills)
    query_response = analeyezer_client.ask_analeyezer(query=query)
    return query_response


def get_courses_from_query(query_response):
    course_list = []
    for course in query_response.json()['top_tags']['buckets']:
        element = course['top_course_hits']['hits']['hits'][0]['_source']
        course_list.append({'course_title': element['course_title'], 'course_id': element['course_id']})
    return course_list
