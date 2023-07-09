import psycopg2

connection = psycopg2.connect('dbname=dbname user=user')
cursor = connection.cursor()


def get_all_mentors():
    cursor.execute('SELECT * FROM mentors ORDER BY id;')
    result = []
    for mentor in cursor.fetchall():
        mentor = list(mentor)
        if len(mentor) != 3:
            mentor.append(None)
        result.append(mentor)
    return result


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
