import faker
from random import randint, choice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import students, subjects, teachers, group, grades

engine = create_engine("postgresql://postgres:stugnap@localhost:5432/postgres client_encoding=utf8")
DBSession = sessionmaker(bind=engine)
session = DBSession()



NUMBER_GROUP = 3
NUMBER_STUDENTS = 30
NUMBER_SUBJECTS = 5
NUMBER_TEACHERS = 5
NUMBER_GRADES = 10

def generate_fake_data(NUMBER_GROUP, NUMBER_STUDENTS, NUMBER_SUBJECTS, NUMBER_TEACHERS, NUMBER_GRADES) -> tuple:
    groups = []  # тут зберігатимемо групи
    students = []  # тут зберігатимемо студентів
    subjects = []  # тут зберігатимемо предмети
    teachers = []  # тут зберігатимемо викладачів
    grades = []  # тут зберігатимемо оцінки

    fake_data = faker.Faker(locale="uk_UA")

    for _ in range(NUMBER_GROUP):
        groups.append(fake_data.land_number())

    for _ in range(NUMBER_STUDENTS):
        students.append(fake_data.name())

    for _ in range(NUMBER_SUBJECTS):
        subjects.append(fake_data.language_name())

    for _ in range(NUMBER_TEACHERS):
        teachers.append(fake_data.name())

    for _ in range(NUMBER_GRADES):
        grades.append(fake_data.random_number())


    return groups, students, subjects, teachers, grades


def prepare_data(students, groups, subjects, teachers, grades) -> tuple:
    
    for_students = []  
    for std in students:
        for_students.append((std, choice(), randint(1, NUMBER_GROUP)))
    
    for_groups = []
    for group in groups:
        for_groups.append((group, randint(1, NUMBER_STUDENTS)))

    for_subjects = []
    for sub in subjects:
        for_subjects.append((sub, randint(1, NUMBER_TEACHERS)))

    for_teachers = []
    for tch in teachers:
        for_teachers.append((tch, randint(1, NUMBER_SUBJECTS)))

    for_grades = []
    for grade in grades:
        for_grades.append((grade, randint(1, NUMBER_STUDENTS)))

    return for_groups, for_students, for_subjects, for_teachers, for_grades
 


def insert_data_to_db(groups, students, subjects, teachers, grades) -> None:
    try:
        # Вставляємо дані про групи
        for group_id in groups:
            new_group = group(id=group_id)
            session.add(new_group)

        # Вставляємо дані про студентів
        for student_name, student_fullname, student_id in students:
            new_student = students(name=student_name, fullname=student_fullname, id=student_id) 
            session.add(new_student)

        # Вставляємо дані про предмети
        for subject_name, teacher_fullname, subjects_id in subjects:
            new_subject = subjects(name=subject_name, teacher_name=teacher_fullname, subject_id=subjects_id) 
            session.add(new_subject)

        # Вставляємо дані про викладачів
        for teacher_name, teacher_fullname, teacher_id in teachers:
            new_teacher = teachers(name=teacher_name, fullname=teacher_fullname, id=teacher_id) 
            session.add(new_teacher)

        # Вставляємо дані про оцінки
        for student_fullname, subject_name, date, grade_value in grades:
            new_grade = grades(student_name=student_fullname, subject_name=subject_name, date_of=date, grade=grade_value)
            session.add(new_grade)

        # Зберігаємо зміни у БД
        session.commit()

    except Exception as e:
        session.rollback()  # У разі помилки відкатуємо зміни
        print(f"Помилка: {e}")

    finally:
        session.close()  # Завершуємо сесію


if __name__ == "__main__":
    groups, students, subjects, teachers, grades = prepare_data(*generate_fake_data(NUMBER_GROUP, NUMBER_STUDENTS, NUMBER_SUBJECTS, NUMBER_TEACHERS))
    insert_data_to_db(groups, students, subjects, teachers, grades)