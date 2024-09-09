from sqlalchemy import select, func, text
from main import *

Base = declarative_base()
def select_1():
    session.query(students.fullname, func.round(func.avg(grades.grade), 2).label('avg_grade'))\
        .select_from(grades).join(students).group_by(students.id).order_by(desc('avg_grade')).limit(5).all()

    pass

def select_2():
    pass

def select_3():
    pass    

def select_4():
    pass    

def select_5():
    pass

def select_6():
    pass

def select_7():
    pass

def select_8():
    pass

def select_9():
    pass

def select_10():
    pass