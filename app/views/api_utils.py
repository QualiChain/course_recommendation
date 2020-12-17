from services.recommendation import Recommendation
import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
log = logging.getLogger(__name__)


def start_recommendation(elk_rec=False, **kwargs):
    """This function decides which type of recommendation is made."""
    try:
        parameters = kwargs['parameters']
        source = parameters['source']
        source_type = parameters['source_type']
        recommendation_type = parameters['recommendation_type']
    except Exception as e:
        log.error(e)
        log.error('Data provided are not in proper format')
        return {"Error": 'Data provided not in proper format'}, 400
    if source_type == 'cv':
        if recommendation_type == 'courses':
            skill_list = [skill['label'] for skill in source['skills']]
            recommender = Recommendation()
            if elk_rec:
                response = recommender.elk_recommend(cv_skills=skill_list)
                recommender.pg_client.session.close()
            else:
                response = recommender.recommend(cv_skills=skill_list)
                recommender.pg_client.session.close()
            return response, 200
        elif recommendation_type == 'skills':
            pass
        elif recommendation_type == 'job_titles':
            pass
    elif source_type == 'skills':
        if recommendation_type == 'courses':
            pass
        elif recommendation_type == 'skills':
            pass
        elif recommendation_type == 'job_titles':
            pass
    elif source_type == 'job_titles':
        if recommendation_type == 'courses':
            pass
        elif recommendation_type == 'skills':
            pass
