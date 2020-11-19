import json

import requests

from settings import SUBMIT_SOURCE, ASK_STORAGE_URI, CURRICULUM_INDEX


class AnalEyeZerClient(object):
    """This Python Object is used to call AnalEyeZer APIs"""

    @staticmethod
    def commit_data_source(**kwargs):
        """
        This function is used to commit data sources to AnalEyeZer

        :param kwargs: provided kwargs
        :return: None
        """
        payload = json.dumps(kwargs)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(
            url=SUBMIT_SOURCE,
            data=payload,
            headers=headers
        )
        return response

    @staticmethod
    def ask_analeyezer(**kwargs):
        """
        This function is used to match courses data

        :param kwargs: provided kwargs
        :return: Matched courses from AnalEyeZer
        """
        if 'query' in kwargs.keys():
            payload = json.dumps(kwargs['query'])
        else:
            payload = []
        headers = {'Content-Type': 'application/json'}

        response = requests.post(
            url=ASK_STORAGE_URI,
            data=payload,
            headers=headers
        )
        return response

    @staticmethod
    def create_elastic_query_for_courses(skill_list):
        '''
        This method creates the query parameters that are sent to the Analeyezer to create and execute the Elastic
        Search query for the recommended courses.
        :param skill_list: list of skills
        :return: query parameters (JSON)
        '''
        skill_list = skill_list
        query_dict = {}
        query_dict['query'] = 'bool_query'
        query_dict['index'] = CURRICULUM_INDEX
        query_dict['min_score'] = 10
        query_dict['_source'] = ["course_id", "course_title"]
        query_dict['should'] = [
            {"multi_match": {
                "query": skill,
                "fields": ["course_description", "dobie_skill_title", "skill_title^3"],
                "type": "phrase",
                "slop": 2
            }} for skill in skill_list]
        query_dict['aggs'] = {
            "top_tags": {
                "terms": {
                    "field": "course_id",
                    "size": 3
                },
                "aggs": {
                    "top_course_hits": {
                        "top_hits": {
                            "sort": [
                                {
                                    "course_id": {
                                        "order": "desc"
                                    }
                                }
                            ],
                            "_source": {
                                "includes": ["course_id", "course_title"]
                            },
                            "size": 1
                        }
                    }
                }
            }
        }
        return query_dict
