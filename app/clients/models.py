from sqlalchemy import Column, Integer, String, Text, DateTime, Float, Boolean, PickleType, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JoinedTableSkillsCourses(Base):
    __tablename__ = "skills_courses_table"

    id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, nullable=False)
    course_title = Column(String(1024), nullable=False)
    course_description = Column(Text, nullable=False)
    skill_id = Column(Integer, nullable=False)
    skill_title = Column(String(1024), nullable=False)


    def __repr__(self):
        return '<JoinedTableSkillsCourses model {}>'.format(self.id)

class Skill(Base):
    __tablename__ = "curriculum_designer_skill"

    id = Column(Integer, primary_key=True, nullable=False)
    skill_name = Column(String(1024), nullable=False)
    skill_title = Column(String(1024), nullable=False)
    skill_type = Column(String(1024), nullable=False)
    hard_skill = Column(Boolean, nullable=True)
    #
    # def __repr__(self):
    #     return '<Skill model {}>'.format(self.id)


class Course(Base):
    __tablename__ = "curriculum_designer_course"

    id = Column(Integer, primary_key=True, nullable=False)
    course_name = Column(String(1024), nullable=False)
    course_title = Column(String(1024), nullable=False)
    course_description = Column(Text, nullable=False)
    course_code = Column(String(1024), nullable=False)
    course_category = Column(String(1024), nullable=False)
    course_class_hours = Column(Integer, nullable=False)
    course_lab_hours = Column(Integer, nullable=False)
    course_credits = Column(Integer, nullable=False)
    course_semester = Column(Integer, nullable=False)
    course_flow_id = Column(Integer, ForeignKey('curriculum_designer_flow.id'))
    course_school_id = Column(Integer, ForeignKey('curriculum_designer_school.id'))

    # def __repr__(self):
    #     return '<Course model {}>'.format(self.id)


class Skill_Course(Base):
    __tablename__ = "curriculum_designer_course_course_skills"

    id = Column(Integer, primary_key=True, nullable=False)
    course_id = Column(Integer, ForeignKey('curriculum_designer_course.id'))
    skill_id = Column(Integer, ForeignKey('curriculum_designer_skill.id'))

    # def __repr__(self):
    #     return '<Skill model {}>'.format(self.id)