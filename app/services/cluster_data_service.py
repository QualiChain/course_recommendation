import pandas as pd
from sqlalchemy import create_engine
import settings
import numpy as np
import json
from utils import execute_elastic_query, get_courses_from_query

from scipy import spatial


class ClusterDataService(object):
    """This Class is used to provide clustering specific information """

    def __init__(self):
        self.engine = create_engine(settings.ENGINE_STRING)

    def get_clustering_skills(self):
        """
        This function is used to get the skills used for clustering from DB

        :return: clustering_skills
        """
        select_query = 'select * from clustering_skills;'

        skills = pd.read_sql_query(select_query, self.engine)
        return skills

    @staticmethod
    def get_centroids_array():
        return np.load('cluster_data/software_job_posts_centroids.npy')

    @staticmethod
    def get_centroid_skills_dict():
        with open('cluster_data/idx_to_skill_dict.json', 'r') as f1:
            idx_to_skills_dict = json.load(f1)
        with open('cluster_data/skill_to_idx_dict.json', 'r') as f2:
            skills_to_idx_dict = json.load(f2)
        return idx_to_skills_dict, skills_to_idx_dict\

    @staticmethod
    def get_cluster_labels_dict():
        with open('cluster_data/centroid_labels.json', 'r') as f2:
            centroid_labels = json.load(f2)
        return centroid_labels

    @staticmethod
    def create_skills_vector_from_list_of_skills(skills, skills_to_idx_dict, num_of_skills):
        x_pred = np.zeros(num_of_skills)

        for s in skills:
            skl_idx = skills_to_idx_dict[s]
            x_pred[skl_idx] = 1
        return x_pred


class RecommenderService(object):
    """ This class is used to  provide recommendations based on clustering info"""

    def __init__(self, skills):
        self.skills = skills
        skill_extractor = ClusterDataService()
        self.clustering_skills = skill_extractor.get_clustering_skills()
        self.centroids_array = skill_extractor.get_centroids_array()
        self.idx_to_skills_dict, self.skills_to_idx_dict = skill_extractor.get_centroid_skills_dict()
        self.num_of_skills = self.centroids_array.shape[1]
        self.user_skills_vector = skill_extractor.create_skills_vector_from_list_of_skills(self.skills, self.skills_to_idx_dict, self.num_of_skills)
        self.closer_clusters = self.get_closer_clusters()
        self.centroid_labels = skill_extractor.get_cluster_labels_dict()

    def get_recommended_skills(self):
        skills_per_cluster = {}
        for c in self.closer_clusters:
            skills_of_c = []
            for sk in np.argsort(-self.centroids_array[c])[0:20]:
                if self.centroids_array[c][sk] <= 0.25:
                    break
                if self.user_skills_vector[sk] == 1:
                    continue
                skills_of_c.append(self.idx_to_skills_dict[str(sk)])
            skills_per_cluster[self.centroid_labels[str(c)]] = skills_of_c

        return skills_per_cluster

    def get_recommended_courses(self):
        rec_skills = self.get_recommended_skills()
        top_skills = []
        for key in rec_skills:
            top_skills += rec_skills[key]
        query_resp = execute_elastic_query(top_skills)
        recommended_courses = get_courses_from_query(query_resp)
        return recommended_courses

    def get_closer_clusters(self):
        distance_vec = np.zeros(11)

        i = 0
        for c in self.centroids_array:
            distance_vec[i] = spatial.distance.cosine(c, self.user_skills_vector)
            i += 1

        return np.argsort(distance_vec)[0:3]

