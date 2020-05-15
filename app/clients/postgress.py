from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker
import pandas as pd

from settings import POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB
from clients.models import Base, JoinedTableSkillsCourses, Skill, Course, Skill_Course


class PostgresClient(object):
    """
    This is a Python Object that handles Postgress DB using SQLAlchemy
    """

    def __init__(self):
        self.engine = create_engine(
            'postgresql+psycopg2://{}:{}@{}/{}'.format(POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_HOST, POSTGRES_DB)
        )
        self.meta = MetaData()
        self.conn = self.engine.connect()
        self.session = sessionmaker(bind=self.engine)()

    def initialize_tables(self):
        # create Tables from Models
        Base.metadata.create_all(self.engine)
        print("Joined table Skills and Courses created successfully")

    def join_skills_and_courses(self):
        res = self.session.query(Course.id, Course.course_title, Course.course_description, Skill.id,
                                 Skill.skill_title).select_from(Course).join(Skill_Course).join(Skill).all()
        return res

    def create_joined_table_skills_courses(self):
        results = self.join_skills_and_courses()

        i = 0
        for row in results:
            record = JoinedTableSkillsCourses(id=i, course_id=row[0], course_title=row[1],
                                              course_description=row[2], skill_id=row[3],
                                              skill_title=row[4])
            self.session.add(record)
            self.session.commit()
            i = i + 1

    # def group_by_variable(self, agg_function, variable):
    #     res = self.session.query()
