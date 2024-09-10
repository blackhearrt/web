import faker
from random import randint, choice
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql://myuser:deadinside666@Homework7:5432/mydatabase")
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


def prepare_data(groups, students, subjects, teachers, grades) -> tuple:
    for_groups = []
    for group in groups:
        for_groups.append((group, ))

    for_students = []  
    for std in students:
        for_students.append((std, choice(), randint(1, NUMBER_GROUP)))

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
    # Створимо з'єднання з нашою БД та отримаємо об'єкт курсору для маніпуляцій з даними

    with sqlite3.connect('salary.db') as con:

        cur = con.cursor()

        '''Заповнюємо таблицю компаній. І створюємо скрипт для вставлення, де змінні, які вставлятимемо, відзначимо
        знаком заповнювача (?) '''

        sql_to_companies = """INSERT INTO companies(company_name)
                               VALUES (?)"""

        '''Для вставлення відразу всіх даних скористаємося методом executemany курсора. Першим параметром буде текст
        скрипта, а другим - дані (список кортежів).'''

        cur.executemany(sql_to_companies, companies)

        # Далі вставляємо дані про співробітників. Напишемо для нього скрипт і вкажемо змінні

        sql_to_employees = """INSERT INTO employees(employee, post, company_id)
                               VALUES (?, ?, ?)"""

        # Дані були підготовлені заздалегідь, тому просто передаємо їх у функцію

        cur.executemany(sql_to_employees, employees)

        # Останньою заповнюємо таблицю із зарплатами

        sql_to_payments = """INSERT INTO payments(employee_id, date_of, total)
                              VALUES (?, ?, ?)"""

        # Вставляємо дані про зарплати

        cur.executemany(sql_to_payments, payments)

        # Фіксуємо наші зміни в БД

        con.commit()


if __name__ == "__main__":
    companies, employees, posts = prepare_data(*generate_fake_data(NUMBER_COMPANIES, NUMBER_EMPLOYESS, NUMBER_POST))
    insert_data_to_db(companies, employees, posts)
