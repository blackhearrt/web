from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

engine = create_engine('sqlite:///:memory:', echo=True)
DBsession = sessionmaker(bind=engine)
session = DBsession()
metadata = MetaData()

students = Table('students', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
)

group_table = Table('group', metadata,
    Column('id', Integer, ForeignKey('students.id')),
    Column('student_name', String, ForeignKey('students.name')),
    
)

teachers = Table('teachers', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
)

subjects = Table('subjects', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('teacher_name', String, ForeignKey('teachers.name')),
)

student_marks = Table('marks', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, ForeignKey('students.name')),
    Column('subject_name', String, ForeignKey('subjects.name')),
    Column('mark', Integer),
    Column('date', String),
)

metadata.create_all(engine)

conn = engine.connect()
result = conn.execute()
conn.close()

