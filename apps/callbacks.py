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


def reset_table(tag, data):

    count_i = 0
    for i in dpg.get_item_children(tag)[1]:
        count_j = 0
        for j in dpg.get_item_children(i)[1]:
            dpg.configure_item(j, default_value=f'{data[count_i][count_j]}')
            count_j += 1
        count_i += 1


def mentor_add_callback(sender, data):
    try:
        add_mentor(dpg.get_value('add_mentor_name'), dpg.get_value('add_mentor_surname'))
        dpg.configure_item('add_mentor_name', default_value='')
        dpg.configure_item('add_mentor_surname', default_value='')
        dpg.configure_item('add_mentor_message', default_value='Успешно создано!', color=(0, 255, 0))
        sleep(5)
        reset_table('mentors_table', get_all_mentors())
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
    reset_table('mentors_table', get_all_mentors())
    dpg.configure_item('edit_mentor_message', default_value='Успешно обновлено!', color=(0, 255, 0))
    sleep(5)
    dpg.configure_item('edit_mentor_message', default_value='Выберите ментора для редактирования',
                       color=(255, 255, 255))


def delete_ok(sender, data, user_data):
    dpg.configure_item(user_data['window_tag'], show=False)
    delete_by_id(user_data['table'], dpg.get_value(user_data['id_tag']))
    sleep(0.5)
    match user_data['table']:
        case 'mentors':
            reset_table(user_data['table_tag'], get_all_mentors())
        case 'payments':
            reset_table(user_data['table_tag'], get_all_payments())


def delete_cancel(sender, data, user_data):
    dpg.configure_item('delete_mentor_modal', show=False)


def mentor_delete_callback(sender, data):
    mentor_name = dpg.get_value('edit_name')

    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        try:
            dpg.get_item_info('delete_mentor_modal')
            dpg.configure_item('delete_mentor_modal', show=True)
            dpg.configure_item('delete_message', default_value=f'Удалить ментора {mentor_name}?')
        except:
            if not dpg.get_value('edit_id'):
                return None

            with dpg.window(label='Удалить?', show=True, tag='delete_mentor_modal', modal=True, no_close=True):
                dpg.add_text(default_value=f'Удалить ментора {mentor_name}?', tag='delete_message')
                with dpg.group(horizontal=True):
                    dpg.add_button(label="Ok", width=75, callback=delete_ok,
                                   user_data={'table': 'mentors', 'id_tag': 'edit_id', 'table_tag': 'mentors_table',
                                              'window_tag': 'delete_mentor_modal'})
                    dpg.add_button(label="Cancel", width=75, callback=delete_cancel)

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
        dpg.configure_item('add_payment_message', default_value='Успешно создано!', color=(0, 255, 0))
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
    for i in get_all_payments():
        i = list(i)
        date = f'{datetime.fromtimestamp(i[-1])}'[:7]
        i[-1] = date
        all_payments.append(i)
    reset_table('payments_table', all_payments)
    dpg.configure_item('edit_payment_message', default_value='Успешно обновлено!', color=(0, 255, 0))
    sleep(5)
    dpg.configure_item('edit_payment_message', default_value='Введите id оплаты для редактирования',
                       color=(255, 255, 255))


def payment_delete_callback(sender, data):
    pass
