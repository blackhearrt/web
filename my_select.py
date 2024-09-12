from sqlalchemy import select, func, text, desc
from sqlalchemy.ext.declarative import declarative_base
from main import *

Base = declarative_base()
def select_1():
    session.query(students.fullname, func.round(func.avg(grades.grade), 2).label('avg_grade'))\
        .select_from(grades).join(students).group_by(students.id).order_by(desc('avg_grade')).limit(5).all()

def select_2():
    session.query(students.fullname).filter_by(grades)\
        .select_from(grades).join(students).group_by(students.id).all().order_by(desc('avg_grade')).limit(1).all()
    

def select_3():
    session.query(
        group.c.id.label('group_id'),
        func.round(func.avg(grades.c.grade_value), 2).label('avg_grade')
    ).join(students, students.c.name == group.c.student_name)\
     .join(grades, grades.c.name_of_student == students.c.name)\
     .filter(grades.c.subject_name == subjects.name, group.c.id == group.id)\
     .group_by(group.c.id).all()
   

def select_4():
    session.query(
        func.round(func.avg(grades.c.grade_value), 2).label('avg_grade')
    ).all()
     

def select_5():
    session.query(
        subjects.c.name.label('subject')
    ).filter(subjects.c.teacher_name == teachers.fullname).all()

def select_6():
    session.query(
        students.c.fullname
    ).join(group, group.c.student_name == students.c.name)\
     .filter(group.c.id == group.id).all()

def select_7():
    session.query(
        students.c.fullname,
        grades.c.grade_value
    ).join(group, group.c.student_name == students.c.name)\
     .join(grades, grades.c.name_of_student == students.c.name)\
     .filter(group.c.id == group.id, grades.c.subject_name == subjects.name).all()

def select_8():
    session.query(
        func.round(func.avg(grades.c.grade_value), 2).label('avg_grade')
    ).join(subjects, subjects.c.name == grades.c.subject_name)\
     .filter(subjects.c.teacher_name == teachers.fullname).all()

def select_9():
    session.query(
        subjects.c.name.label('course')
    ).join(grades, grades.c.subject_name == subjects.c.name)\
     .filter(grades.c.students_name == students.fullname).all()

def select_10():
    session.query(
        subjects.c.name.label('course')
    ).join(grades, grades.c.subject_name == subjects.c.name)\
     .filter(grades.c.students_name == students.fullname, subjects.c.teacher_name == teachers.fullname).all()