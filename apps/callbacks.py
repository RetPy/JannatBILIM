from datetime import datetime
from time import sleep

import dearpygui.dearpygui as dpg

from utils.db import (add_mentor,
                      edit_mentor,
                      add_payment,
                      edit_payment,
                      get_all_mentors,
                      get_all_payments,
                      get_mentor_id_by_name,
                      get_mentor_by_name,
                      get_payment_by_id,
                      delete_by_id)


def set_table(table_tag, parent_tag, columns, data):
    dpg.delete_item(table_tag)
    with dpg.table(header_row=True, tag=table_tag, no_host_extendY=True, scrollY=True, parent=parent_tag,
                   borders_outerH=True, borders_innerV=True, borders_innerH=True, borders_outerV=True):
        for col in columns:
            if col == 'id':
                dpg.add_table_column(label='id', width_fixed=True)
                continue
            dpg.add_table_column(label=col)

        for item in data:
            with dpg.table_row():
                for i in range(len(columns)):
                    dpg.add_text(default_value=item[i])


def mentor_add_callback(sender, data):
    try:
        add_mentor(dpg.get_value('add_mentor_name'), dpg.get_value('add_mentor_surname'))
        dpg.configure_item('add_mentor_name', default_value='')
        dpg.configure_item('add_mentor_surname', default_value='')
        dpg.configure_item('add_mentor_message', default_value='Успешно создано!', color=(0, 255, 0))
        dpg.configure_item('mentor_choose', items=[i[1] for i in get_all_mentors()])
        set_table('mentors_table', 'mentors_window', ('id', 'Имя', 'Фамилия'), get_all_mentors())
        sleep(5)
        dpg.configure_item('add_mentor_message', default_value='Заполните поля для создания ментора',
                           color=(255, 255, 255))
    except:
        dpg.configure_item('add_mentor_message', default_value='Внутренняя ошибка!', color=(255, 0, 0))


def mentor_choose_callback(sender, data):
    mentor = get_mentor_by_name(dpg.get_value('mentor_choose'))
    dpg.configure_item('edit_id', default_value=mentor[0])
    dpg.configure_item('edit_name', default_value=mentor[1])
    dpg.configure_item('edit_surname', default_value=mentor[2])


def mentor_edit_callback(sender, data):
    mentor_id = dpg.get_value('edit_id')
    name = dpg.get_value('edit_name')
    surname = dpg.get_value('edit_surname')
    edit_mentor(mentor_id, name, surname)
    dpg.configure_item('mentor_choose', items=[i[1] for i in get_all_mentors()])
    set_table('mentors_table', 'mentors_window', ('id', 'Имя', 'Фамилия'), get_all_mentors())
    dpg.configure_item('edit_mentor_message', default_value='Успешно обновлено!', color=(0, 255, 0))
    sleep(5)
    dpg.configure_item('edit_mentor_message', default_value='Выберите ментора для редактирования',
                       color=(255, 255, 255))


def delete_ok(sender, data, user_data):
    dpg.configure_item(user_data['window_tag'], show=False)
    delete_by_id(user_data['table'], dpg.get_value(user_data['id_tag']))

    all_payments = []
    for payment in get_all_payments():
        payment = list(payment)
        date = datetime.fromtimestamp(payment[-1])
        payment[-1] = f'{date}'[:7]
        all_payments.append(payment)

    match user_data['table']:
        case 'mentors':
            dpg.configure_item('mentor_choose', items=[i[1] for i in get_all_mentors()], default_value='Ментор')
            dpg.configure_item('edit_id', default_value='')
            dpg.configure_item('edit_name', default_value='')
            dpg.configure_item('edit_surname', default_value='')
            set_table(user_data['table_tag'], 'mentors_window', ('id', 'Имя', 'Фамилия'), get_all_mentors())
        case 'payments':
            dpg.configure_item('edit_payment_id', default_value='')
            dpg.configure_item('edit_payment_name', default_value='Имя ментора')
            dpg.configure_item('edit_payment_price', default_value='')
            dpg.configure_item('edit_payment_date', default_value='')
            set_table(user_data['table_tag'], 'payments_window', ('id', 'Имя Ментора', 'Сумма', 'Дата'), all_payments)


def delete_cancel(sender, data, user_data):
    dpg.configure_item(user_data['window_tag'], show=False)


def mentor_delete_callback(sender, data):
    mentor_name = dpg.get_value('edit_name')

    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        try:
            dpg.get_item_info('delete_mentor_modal')
            dpg.configure_item('delete_mentor_modal', show=True)
            dpg.configure_item('delete_mentor_message', default_value=f'Удалить ментора {mentor_name}?')
        except:
            if not dpg.get_value('edit_id'):
                return None

            with dpg.window(label='Удалить?', show=True, tag='delete_mentor_modal', modal=True, no_close=True):
                dpg.add_text(default_value=f'Удалить ментора {mentor_name}?', tag='delete_mentor_message')
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Ok", width=75, callback=delete_ok,
                                   user_data={'table': 'mentors', 'id_tag': 'edit_id', 'table_tag': 'mentors_table',
                                              'window_tag': 'delete_mentor_modal'})
                    dpg.add_button(label="Cancel", width=75, callback=delete_cancel,
                                   user_data={'window_tag': 'delete_mentor_modal'})

    dpg.split_frame()
    width = dpg.get_item_width('delete_mentor_modal')
    height = dpg.get_item_height('delete_mentor_modal')
    dpg.set_item_pos('delete_mentor_modal', [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])


def payment_add_callback(sender, data):
    try:
        mentor_id = get_mentor_id_by_name(name=dpg.get_value('add_payment_mentor_name'))
        price = dpg.get_value('add_payment_price')
        date = list(map(int, dpg.get_value('add_payment_date').split('.')))
        add_payment(mentor_id, price, date[0], date[1])
        dpg.configure_item('add_payment_mentor_name', default_value='Имя ментора')
        dpg.configure_item('add_payment_price', default_value='')
        dpg.configure_item('add_payment_date', default_value='')
        dpg.configure_item('add_payment_message', default_value='Успешно создано!', color=(0, 255, 0))

        all_payments = []
        for payment in get_all_payments():
            payment = list(payment)
            date = datetime.fromtimestamp(payment[-1])
            payment[-1] = f'{date}'[:7]
            all_payments.append(payment)

        set_table('payments_table', 'payments_window', ('id', 'Имя Ментора', 'Сумма', 'Дата'), all_payments)
        sleep(5)
        dpg.configure_item('add_payment_message', default_value='Заполните поля для создания оплаты',
                           color=(255, 255, 255))
    except ValueError:
        dpg.configure_item('add_payment_message', default_value='Неверный формат даты!', color=(255, 0, 0))
        sleep(10)
        dpg.configure_item('add_payment_message', default_value='Заполните поля для создания оплаты',
                           color=(255, 255, 255))
    except:
        dpg.configure_item('add_payment_message', default_value='Внутренняя ошибка!', color=(255, 0, 0))


def payment_choose_callback(sender, data):
    payment = get_payment_by_id(dpg.get_value('edit_payment_id'))
    if payment:
        date = '.'.join(f'{datetime.fromtimestamp(payment[3])}'[:7].split('-'))
        dpg.configure_item('edit_payment_name', default_value=payment[1])
        dpg.configure_item('edit_payment_price', default_value=payment[2])
        dpg.configure_item('edit_payment_date', default_value=date)
        dpg.configure_item('edit_payment_message', default_value='Введите id оплаты для редактирования',
                           color=(255, 255, 255))
    else:
        dpg.configure_item('edit_payment_message', default_value='Не найдено!', color=(255, 0, 0))


def payment_edit_callback(sender, data):
    payment_id = dpg.get_value('edit_payment_id')
    payment_mentor_id = get_mentor_id_by_name(dpg.get_value('edit_payment_name'))
    payment_price = dpg.get_value('edit_payment_price')
    try:
        date = list(map(int, dpg.get_value('edit_payment_date').split('.')))
        edit_payment(payment_id, payment_mentor_id, payment_price, date[0], date[1])
    except ValueError:
        dpg.configure_item('edit_payment_message', default_value='Неверный формат даты!', color=(255, 0, 0))
        sleep(10)
        dpg.configure_item('edit_payment_message', default_value='Введите id оплаты для редактирования',
                           color=(255, 255, 255))
        return None

    all_payments = []
    for payment in get_all_payments():
        payment = list(payment)
        date = datetime.fromtimestamp(payment[-1])
        payment[-1] = f'{date}'[:7]
        all_payments.append(payment)

    set_table('payments_table', 'payments_window', ('id', 'Имя Ментора', 'Сумма', 'Дата'), all_payments)
    dpg.configure_item('edit_payment_message', default_value='Успешно обновлено!', color=(0, 255, 0))
    sleep(5)
    dpg.configure_item('edit_payment_message', default_value='Введите id оплаты для редактирования',
                       color=(255, 255, 255))


def payment_delete_callback(sender, data):
    payment_id = dpg.get_value('edit_payment_id')

    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        try:
            dpg.get_item_info('delete_payment_modal')
            dpg.configure_item('delete_payment_modal', show=True)
            dpg.configure_item('delete_payment_message', default_value=f'Удалить оплату {payment_id}?')
        except:
            if not dpg.get_value('edit_payment_id'):
                return None

            with dpg.window(label='Удалить?', show=True, tag='delete_payment_modal', modal=True, no_close=True):
                dpg.add_text(default_value=f'Удалить оплату {payment_id}?', tag='delete_payment_message')
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Ok", width=75, callback=delete_ok,
                                   user_data={'table': 'payments', 'id_tag': 'edit_payment_id',
                                              'table_tag': 'payments_table', 'window_tag': 'delete_payment_modal'})
                    dpg.add_button(label="Cancel", width=75, callback=delete_cancel,
                                   user_data={'window_tag': 'delete_payment_modal'})

    dpg.split_frame()
    width = dpg.get_item_width('delete_payment_modal')
    height = dpg.get_item_height('delete_payment_modal')
    dpg.set_item_pos('delete_payment_modal', [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])
