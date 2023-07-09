from datetime import datetime

import psycopg2
from psycopg2.extensions import AsIs

connection = psycopg2.connect('dbname=dbname user=user')
cursor = connection.cursor()


def delete_by_id(table_name, id_):
    cursor.execute(
        'DELETE FROM %s WHERE id=%s',
        (AsIs(table_name), id_,)
    )
    connection.commit()


def get_all_mentors():
    cursor.execute('SELECT * FROM mentors ORDER BY id;')
    result = []
    for mentor in cursor.fetchall():
        mentor = list(mentor)
        if len(mentor) != 3:
            mentor.append(None)
        result.append(mentor)
    return result


def get_mentor_id_by_name(name: str):
    try:
        cursor.execute(
            'SELECT id FROM mentors WHERE name=%s',
            (name,)
        )
        return cursor.fetchone()[0]
    except TypeError:
        return None


def get_mentor_by_name(name: str):
    try:
        cursor.execute(
            'SELECT * FROM mentors WHERE name=%s',
            (name,)
        )
        return cursor.fetchone()
    except TypeError:
        return None


def add_mentor(name=None, surname=None):
    cursor.execute(
        'INSERT INTO mentors (name, surname) VALUES (%s, %s)',
        (name, surname)
    )

    connection.commit()


def edit_mentor(mentor_id, name, surname):
    cursor.execute(
        'UPDATE mentors SET name=%s, surname=%s WHERE id=%s',
        (name, surname, mentor_id)
    )
    connection.commit()


def get_all_payments(group_by=False):
    if group_by:
        cursor.execute(
            'SELECT date, SUM(price) FROM payments GROUP BY date;'
        )
    else:
        cursor.execute(
            '''SELECT payments.id, mentors.name, price, date
            FROM payments
            JOIN mentors
            ON payments.mentor_id = mentors.id
            ORDER BY payments.id;'''
        )
    if group_by:
        date = []
        price = []
        for i in cursor.fetchall():
            date.append(i[0])
            price.append(i[1])
        return date, price
    return cursor.fetchall()


def get_payment_by_id(payment_id):
    cursor.execute(
        '''SELECT payments.id, mentors.name, price, date
        FROM payments
        JOIN mentors
        ON payments.mentor_id = mentors.id
        WHERE payments.id=%s;''',
        (payment_id,)
    )
    result = cursor.fetchone()
    return result


def get_mentors_payments(mentor_id):
    cursor.execute(
        'SELECT date, SUM(price) FROM payments WHERE mentor_id=%s GROUP BY date;',
        (mentor_id,)
    )

    date = []
    price = []
    for i in cursor.fetchall():
        date.append(i[0])
        price.append(i[1])
    return date, price


def add_payment(mentor_id: int, price: int, year: int, month: int):
    cursor.execute(
        'INSERT INTO payments (mentor_id, price, date) VALUES (%s, %s, %s);',
        (mentor_id, price, datetime.timestamp(datetime(year, month, 1)))
    )
    connection.commit()
    print('OK | Payment added!')


def edit_payment(payment_id, mentor_id, price, year, month):
    cursor.execute(
        'UPDATE payments SET mentor_id=%s, price=%s, date=%s WHERE id=%s',
        (mentor_id, price, datetime.timestamp(datetime(year, month, 1)), payment_id)
    )
    connection.commit()


if __name__ == '__main__':
    print(get_all_mentors())
    print(get_all_payments())
    print(get_mentors_payments(1))
    print(get_mentor_id_by_name('Гульнара'))
    print(get_payment_by_id(17))