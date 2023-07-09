import dearpygui.dearpygui as dpg

from datetime import datetime

from utils.db import get_all_payments, get_all_mentors, get_mentors_payments


def make_graphs():
    with dpg.plot(label='График', height=-1, width=-1):
        all_payments = get_all_payments(group_by=True)

        dpg.add_plot_legend(label='Payments Graphs')

        dpg.add_plot_axis(dpg.mvXAxis, label="Дата", time=True)
        dpg.set_axis_limits(
            dpg.last_item(),
            datetime.timestamp(datetime(2022, 1, 1)),
            datetime.timestamp(datetime.now()),
        )
        dpg.add_plot_axis(dpg.mvYAxis, label="Доход", tag="y_axis", lock_min=True)

        dpg.add_shade_series(all_payments[0], all_payments[1], label="Весь", parent="y_axis")
        for mentor in get_all_mentors():
            data = get_mentors_payments(mentor[0])
            if bool(data[0]) is False or bool(data[1]) is False:
                continue
            dpg.add_shade_series(data[0], data[1], label=f'{mentor[0]}.{mentor[1]}', parent='y_axis')


if __name__ == '__main__':
    pass
