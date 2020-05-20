import logging
import sys

from flask import Flask, jsonify, request
from flask_cors import CORS

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
        status = '500'

    results = {'status': status, 'results': results}

    return jsonify(results)
