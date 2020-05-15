import json

import requests

from app.settings import SUBMIT_SOURCE


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
