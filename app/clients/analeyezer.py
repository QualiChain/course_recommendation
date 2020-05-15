import json

import requests

from settings import SUBMIT_SOURCE, ASK_STORAGE_URI


class AnalEyeZerClient(object):
    """This Python Object is used to call AnalEyeZer APIs"""

    @staticmethod
    def commit_data_source(**kwargs):
        """
        This function is used to commit data sources to AnalEyeZer

        :param kwargs: provided kwargs
        :return: None
        """
        payload = json.dumps(**kwargs)
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
        payload = json.dumps(**kwargs)
        headers = {'Content-Type': 'application/json'}

        response = requests.post(
            url=ASK_STORAGE_URI,
            data=payload,
            headers=headers
        )
        return response
