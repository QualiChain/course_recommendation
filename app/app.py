from services.cluster_data_service import  RecommenderService
from flask_restful import Resource, Api
from flask import request, Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

api = Api(app)


class PersonalisedSkillsRecommendation(Resource):

    def post(self):
        data = request.get_json()
        user_skills = data['Skills']

        skill_names = []
        for s in user_skills:
            skill_names.append(s['SkillLabel'])

        recommender_service = RecommenderService(skill_names)
        recommended_skills = recommender_service.get_recommended_skills()
        return recommended_skills, 201


api.add_resource(PersonalisedSkillsRecommendation, '/skills_recommendation')
