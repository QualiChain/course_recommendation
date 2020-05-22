import logging
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS
from services.recommendation import Recommendation

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)

'''Run flask by executing the command python -m flask run'''

app = Flask(__name__)
CORS(app)


@app.route('/get_skills_from_cv', methods=['POST'])
def get_skills_from_cv():
    '''
    This api call reads a CV and returns the included skills.
    Post body(json):
    {}
    :return: Returns a list of skills in JSON format.
    '''

    cv = request.get_json()
    try:
        skill_list = [skill['SkillLabel'] for skill in cv['Skills']]
        recommender = Recommendation()
        response = recommender.recommend(cv_skills=skill_list)
        return response, 200
    except Exception as ex:
        log.error(ex)
        return ex, 400

