from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Student, Group, Teacher, Subject, Grade, create_random_data

engine = create_engine('sqlite:///university.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

num_students = 50
num_groups = 3
num_subjects = 8
num_teachers = 5

create_random_data(session, num_students, num_groups, num_subjects, num_teachers)
