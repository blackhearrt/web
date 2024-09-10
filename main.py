from sqlalchemy import Table, Column, Integer, String, ForeignKey, MetaData, create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('postgresql://myuser:deadinside666@Homework7:5432/mydatabase', echo=True)
DBsession = sessionmaker(bind=engine)
session = DBsession()
metadata = MetaData()

students = Table('students', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('fullname', String),
)

group = Table('group', metadata,
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

grades = Table('grades', metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, ForeignKey('students.name')),
    Column('subject_name', String, ForeignKey('subjects.name')),
    Column('grade', Integer),
    Column('date', String),
)

metadata.create_all(engine)

conn = engine.connect()
result = conn.execute()
conn.close()

