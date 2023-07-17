import dearpygui.dearpygui as dpg

from datetime import datetime

from utils.db import get_all_mentors, get_all_payments
from apps.callbacks import (set_table,
                            mentor_add_callback,
                            mentor_choose_callback,
                            mentor_edit_callback,
                            mentor_delete_callback,
                            payment_add_callback,
                            payment_choose_callback,
                            payment_edit_callback,
                            payment_delete_callback)


def mentor_add_form():
    with dpg.table(header_row=False):
        for i in range(5):
            dpg.add_table_column()
        for i in range(5):
            with dpg.table_row():
                dpg.add_text('')
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_text(default_value='Заполните поля для создания ментора', tag='add_mentor_message')
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(hint='Имя', tag='add_mentor_name', width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(hint='Фамилия', tag='add_mentor_surname', width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_button(label='Создать', tag='create', callback=mentor_add_callback)


def mentor_edit_form():
    all_mentors = get_all_mentors()
    with dpg.table(header_row=False):
        dpg.add_table_column()
        dpg.add_table_column()
        dpg.add_table_column(width_fixed=True)
        dpg.add_table_column()
        dpg.add_table_column()
        with dpg.table_row():
            dpg.add_text('')
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_text(default_value='Выберите ментора для редактирования', tag='edit_mentor_message')
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_combo([i[1] for i in all_mentors], tag='mentor_choose', width=300, default_value='Ментор')
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(tag='edit_id', hint='id', width=300, enabled=False, readonly=True)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(tag='edit_name', hint='Имя', width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(tag='edit_surname', hint='Фамилия', width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            with dpg.group(horizontal=True):
                dpg.add_button(label='Найти', callback=mentor_choose_callback)
                dpg.add_button(label='Изменить', callback=mentor_edit_callback)
                dpg.add_button(label='Удалить', callback=mentor_delete_callback)
        with dpg.table_row():
            dpg.add_text('')
    dpg.add_button(label='Test', callback=test_callback)

    with dpg.child_window(tag='mentors_window', border=False):
        set_table('mentors_table', 'mentors_window', ('id', 'Имя', 'Фамилия'), all_mentors)


def payment_add_form():
    with dpg.table(header_row=False):
        for i in range(5):
            dpg.add_table_column()
        for i in range(5):
            with dpg.table_row():
                dpg.add_text('')
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_text(default_value='Заполните поля для создания', tag='add_payment_message')
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_combo([i[1] for i in get_all_mentors()], default_value='Имя ментора', tag='add_payment_mentor_name', width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(hint='Сумма', tag='add_payment_price', width=300, decimal=True)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(hint='ГГГГ.ММ', tag='add_payment_date', decimal=True, width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_button(label='Создать', callback=payment_add_callback)


def payment_edit_form():
    all_payments = []
    all_mentors = get_all_mentors()
    for payment in get_all_payments():
        payment = list(payment)
        date = datetime.fromtimestamp(payment[-1])
        payment[-1] = f'{date}'[:7]
        all_payments.append(payment)

    with dpg.table(header_row=False):
        dpg.add_table_column()
        dpg.add_table_column()
        dpg.add_table_column(width_fixed=True)
        dpg.add_table_column()
        dpg.add_table_column()
        with dpg.table_row():
            dpg.add_text('')
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_text(default_value='Введите id оплаты для редактирования', tag='edit_payment_message')
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(tag='edit_payment_id', hint='id', width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_combo([i[1] for i in all_mentors], tag='edit_payment_name', default_value='Имя ментора', width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(tag='edit_payment_price', hint='Сумма', decimal=True, width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            dpg.add_input_text(tag='edit_payment_date', hint='ГГГГ.ММ', decimal=True, width=300)
        with dpg.table_row():
            dpg.add_text('')
            dpg.add_text('')
            with dpg.group(horizontal=True):
                dpg.add_button(label='Найти', callback=payment_choose_callback)
                dpg.add_button(label='Изменить', callback=payment_edit_callback)
                dpg.add_button(label='Удалить', callback=payment_delete_callback)
        with dpg.table_row():
            dpg.add_text('')

    with dpg.child_window(tag='payments_window', border=False):
        set_table('payments_tag', 'payments_window', ('id', 'Имя Ментора', 'Сумма', 'Дата'), all_payments)


if __name__ == '__main__':
    pass
