from datetime import datetime
import sqlite3

connection = sqlite3.connect('jannat_bilim.sqlite', check_same_thread=False)
cursor = connection.cursor()


def delete_by_id(table_name, id_):
    sql = f'DELETE FROM {table_name} WHERE id={id_}'
    cursor.execute(sql)
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
            'SELECT id FROM mentors WHERE name=?',
            (name,)
        )
        return cursor.fetchone()[0]
    except TypeError:
        return None


def get_mentor_by_name(name: str):
    try:
        cursor.execute(
            'SELECT * FROM mentors WHERE name=?',
            (name,)
        )
        return cursor.fetchone()
    except TypeError:
        return None


def add_mentor(name=None, surname=None):
    cursor.execute(
        'INSERT INTO mentors (name, surname) VALUES (?, ?)',
        (name, surname)
    )
    connection.commit()


def edit_mentor(mentor_id, name, surname):
    cursor.execute(
        'UPDATE mentors SET name=?, surname=? WHERE id=?',
        (name, surname, mentor_id)
    )
    connection.commit()


def get_all_payments(group_by=False):
    if group_by:
        cursor.execute(
            'SELECT date, SUM(price) FROM payments GROUP BY date ORDER BY date;'
        )
    else:
        cursor.execute(
            '''SELECT payments.id, mentors.name, price, date
            FROM payments
            JOIN mentors
            ON payments.mentor_id = mentors.id
            ORDER BY payments.id;'''
        )
    result = cursor.fetchall()
    if group_by:
        date = []
        price = []
        for i in result:
            date.append(i[0])
            price.append(i[1])
        return date, price
    return result


def get_payment_by_id(payment_id):
    cursor.execute(
        '''SELECT payments.id, mentors.name, price, date
        FROM payments
        JOIN mentors
        ON payments.mentor_id = mentors.id
        WHERE payments.id=?;''',
        (payment_id,)
    )
    result = cursor.fetchone()
    return result


def get_mentors_payments(mentor_id):
    cursor.execute(
        'SELECT date, SUM(price) FROM payments WHERE mentor_id=? GROUP BY date ORDER BY date;',
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
        'INSERT INTO payments (mentor_id, price, date) VALUES (?, ?, ?);',
        (mentor_id, price, datetime.timestamp(datetime(year, month, 1)))
    )
    connection.commit()
    print('OK | Payment added!')


def edit_payment(payment_id, mentor_id, price, year, month):
    cursor.execute(
        'UPDATE payments SET mentor_id=?, price=?, date=? WHERE id=?',
        (mentor_id, price, datetime.timestamp(datetime(year, month, 1)), payment_id)
    )
    connection.commit()


if __name__ == '__main__':
    pass
    # add_mentor('test', 'test')
    # delete_by_id('mentors', 22)
    # print(get_all_mentors())
    # print(get_all_payments(group_by=True))
    # print(get_mentors_payments(1))
    # print(get_mentor_id_by_name('Гульнара'))
    # print(get_payment_by_id(17))
