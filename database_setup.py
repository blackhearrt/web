from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from faker import Faker
import random

Base = declarative_base()
faker = Faker()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Student(id={self.id}, name={self.name})>"

class Group(Base):
    __tablename__ = 'groups'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Group(id={self.id}, name={self.name})>"

class Teacher(Base):
    __tablename__ = 'teachers'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)

    def __repr__(self):
        return f"<Teacher(id={self.id}, name={self.name})>"

class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    teacher_id = Column(Integer, ForeignKey('teachers.id'))

    teacher = relationship("Teacher", back_populates="subjects")

    def __repr__(self):
        return f"<Subject(id={self.id}, name={self.name}, teacher_id={self.teacher_id})>"

class Grade(Base):
    __tablename__ = 'grades'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    score = Column(Float)

    student = relationship("Student", back_populates="grades")
    subject = relationship("Subject", back_populates="grades")

    def __repr__(self):
        return f"<Grade(id={self.id}, student_id={self.student_id}, subject_id={self.subject_id}, score={self.score})>"

Student.grades = relationship("Grade", back_populates="student")
Group.students = relationship("Student", back_populates="group")
Teacher.subjects = relationship("Subject", back_populates="teacher")
Subject.grades = relationship("Grade", back_populates="subject")

def create_random_data(session, num_students, num_groups, num_subjects, num_teachers):
    students = [Student(name=faker.name()) for _ in range(num_students)]
    groups = [Group(name=f"Group {i+1}") for i in range(num_groups)]
    teachers = [Teacher(name=faker.name()) for _ in range(num_teachers)]
    subjects = [Subject(name=f"Subject {i+1}", teacher=random.choice(teachers)) for i in range(num_subjects)]

    for student in students:
        student.group = random.choice(groups)
        session.add(student)

    for group in groups:
        session.add(group)

    for teacher in teachers:
        session.add(teacher)

    for subject in subjects:
        session.add(subject)

    session.commit()

if __name__ == "__main__":
    engine = create_engine('sqlite:///university.db')
    Base.metadata.create_all(engine)

