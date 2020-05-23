import logging
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

from services.cluster_data_service import RecommenderService
from flask_restful import Resource, Api


app = Flask(__name__)
CORS(app)

api = Api(app)

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
    if cv is not None:
        skill_list = [skill['SkillLabel'] for skill in cv['Skills']]
        results = {'skills': skill_list}
        status = '200'
    else:
        description = 'Incorrect Request'
        results = {}
        status = '400'

    results = {'status': status, 'results': results}

    return jsonify(results)


@app.route('/get_recommended_skills', methods=['POST'])
def get_recommended_skills():
    data = request.get_json()
    user_skills = data['Skills']

    skill_names = []
    for s in user_skills:
        skill_names.append(s['SkillLabel'])

    recommender_service = RecommenderService(skill_names)
    recommended_skills = recommender_service.get_recommended_skills()
    return jsonify(recommended_skills)


@app.route('/get_recommended_courses', methods=['POST'])
def get_recommended_courses():
    data = request.get_json()
    user_skills = data['Skills']

    skill_names = []
    for s in user_skills:
        skill_names.append(s['SkillLabel'])

    recommender_service = RecommenderService(skill_names)
    recommended_courses = recommender_service.get_recommended_courses()
    return jsonify(recommended_courses)

