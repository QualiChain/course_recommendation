import logging

from flask import Flask, jsonify, request
from flask_cors import CORS

import sys

from views.api_utils import start_recommendation

from services.cluster_data_service import RecommenderService

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
    It ustilises both the clustering and the ELK recommendation logic
    '''

    parameters = request.get_json()
    try:
        response = start_recommendation(parameters=parameters)
        return response
    except Exception as ex:
        log.error(ex)
        return ex, 400


@app.route('/recommend_elk', methods=['POST'])
def elk_recommend():
    '''
    This api call reads a CV, list of skills or job tiles and returns recommended skills, courses or job titles.
    Post body(json):
    {"source":{--source, for example a CV},
    "source_type": "cv, skills or job_titles",
    "recommendation_type": "courses, skills or job_titles"}
    :return: Returns a list of recommended assets in JSON format using the elasticsearch recommendationlogic.
    '''

    parameters = request.get_json()
    try:
        response = start_recommendation(elk_rec=True, parameters=parameters)
        return response
    except Exception as ex:
        log.error(ex)
        return ex, 400


@app.route('/get_recommended_skills', methods=['POST'])
def get_recommended_skills():
    data = request.get_json()
    user_skills = data['skills']

    skill_names = []
    for s in user_skills:
        skill_names.append(s['label'])

    recommender_service = RecommenderService(skill_names)
    recommended_skills = recommender_service.get_recommended_skills()
    recommender_service.pg_client.engine.dispose()
    recommender_service.pg_client.qualichain_db_engine.dispose()
    return jsonify(recommended_skills)


@app.route('/get_recommended_courses', methods=['POST'])
def get_recommended_courses():
    data = request.get_json()
    user_skills = data['skills']

    skill_names = []
    for s in user_skills:
        skill_names.append(s['label'])

    recommender_service = RecommenderService(skill_names)
    recommended_courses = recommender_service.get_recommended_courses()
    recommender_service.pg_client.engine.dispose()
    recommender_service.pg_client.qualichain_db_engine.dispose()
    return jsonify(recommended_courses)
