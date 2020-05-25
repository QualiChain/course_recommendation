import logging
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

import sys

from views.api_utils import start_recommendation

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

'''Run flask by executing the command python -m flask run'''

app = Flask(__name__)
CORS(app)


@app.route('/recommend', methods=['POST'])
def recommend():
    '''
    This api call reads a CV, list of skills or job tiles and returns recommended skills, courses or job titles.
    Post body(json):
    {"source":{--source, for example a CV},
    "source_type": "cv, skills or job_titles",
    "recommendation_type": "courses, skills or job_titles"}
    :return: Returns a list of recommended assets in JSON format.
    '''

    parameters = request.get_json()
    try:
        response = start_recommendation(parameters=parameters)
        return response
    except Exception as ex:
        log.error(ex)
        return ex, 400
