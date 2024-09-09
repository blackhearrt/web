from datetime import datetime
import faker
from random import randint, choice
from sqlalchemy.orm import sessionmaker

NUMBER_GROUP = 3
NUMBER_STUDENTS = 30
NUMBER_SUBJECTS = 5
NUMBER_TEACHERS = 5
NUMBER_GRADES = 10

def generate_fake_data(NUMBER_GROUP, NUMBER_STUDENTS, NUMBER_SUBJECTS, NUMBER_TEACHERS, NUMBER_GRADES) -> tuple():
    groups = []  # тут зберігатимемо компанії
    students = []  # тут зберігатимемо співробітників
    subjects = []  # тут зберігатимемо посади
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


def prepare_data(groups, students, subjects, teachers, grades) -> tuple():
    for_groups = []
    # готуємо список кортежів номерів груп
    for group in groups:
        for_groups.append((group, ))

    for_students = []  # для таблиці students

    for std in students:
        '''
        Для записів у таблицю співробітників нам потрібно додати посаду та id компанії. Компаній у нас було за замовчуванням
        NUMBER_COMPANIES, при створенні таблиці companies для поля id ми вказували INTEGER AUTOINCREMENT - тому кожен
        запис отримуватиме послідовне число збільшене на 1, починаючи з 1. Тому компанію вибираємо випадково
        у цьому діапазоні
        '''
        for_students.append((std, choice(), randint(1, NUMBER_GROUP)))

    '''
   Подібні операції виконаємо й у таблиці payments виплати зарплат. Приймемо, що виплата зарплати у всіх компаніях
    виконувалася з 10 по 20 числа кожного місяця. Діапазон зарплат генеруватимемо від 1000 до 10000 у.о.
    для кожного місяця, та кожного співробітника.
    '''
    for_payments = []

    for month in range(1, 12 + 1):
        # Виконуємо цикл за місяцями'''
        payment_date = datetime(2021, month, randint(10, 20)).date()
        for emp in range(1, NUMBER_EMPLOYESS + 1):
            # Виконуємо цикл за кількістю співробітників
            for_payments.append((emp, payment_date, randint(1000, 10000)))

    return for_companies, for_employees, for_payments


def insert_data_to_db(companies, employees, payments) -> None:
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
