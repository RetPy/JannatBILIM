import dearpygui.dearpygui as dpg

from datetime import datetime
from random import choice

from utils.db import get_all_payments, get_all_mentors, get_mentors_payments

TRANSPARENCY = 80
COLOR_RGB = (
    (255, 0, 0, TRANSPARENCY),
    (0, 255, 0, TRANSPARENCY),
    (0, 0, 255, TRANSPARENCY),
    (153, 0, 153, TRANSPARENCY),
    (255, 255, 0, TRANSPARENCY),
    (255, 128, 0, TRANSPARENCY),
    (255, 0, 255, TRANSPARENCY),
    (0, 255, 255, TRANSPARENCY),
    (255, 0, 127, TRANSPARENCY),
    (128, 255, 0, TRANSPARENCY),
)


def make_graphs():
    with dpg.plot(label='График', height=-1, width=-1):
        all_payments = get_all_payments(group_by=True)

        dpg.add_plot_legend(label='Payments Graphs')

        dpg.add_plot_axis(dpg.mvXAxis, label="Дата", time=True)
        dpg.set_axis_limits(
            dpg.last_item(),
            datetime.timestamp(datetime(2022, 6, 1)),
            datetime.timestamp(datetime.now()),
        )
        dpg.add_plot_axis(dpg.mvYAxis, label="Доход", tag="y_axis", lock_min=True)

        dpg.add_shade_series(all_payments[0], all_payments[1], label="Весь", parent="y_axis", tag='all_payments')

        with dpg.theme(tag='all_payments_theme'):
            with dpg.theme_component(0):
                dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255), category=dpg.mvThemeCat_Plots)
                dpg.add_theme_color(dpg.mvPlotCol_Fill, (0, 128, 255, TRANSPARENCY), category=dpg.mvThemeCat_Plots)

        dpg.bind_item_theme('all_payments', 'all_payments_theme')

        for mentor in get_all_mentors():
            data = get_mentors_payments(mentor[0])
            if bool(data[0]) is False or bool(data[1]) is False:
                continue
            dpg.add_shade_series(data[0], data[1], label=f'{mentor[0]}.{mentor[1]}', parent='y_axis',
                                 tag=f'{mentor[1]}_series')

            with dpg.theme(tag=f'{mentor[1]}_theme'):
                with dpg.theme_component(0):
                    dpg.add_theme_color(dpg.mvPlotCol_Line, (255, 255, 255), category=dpg.mvThemeCat_Plots)
                    dpg.add_theme_color(dpg.mvPlotCol_Fill, choice(COLOR_RGB), category=dpg.mvThemeCat_Plots)

            dpg.bind_item_theme(f'{mentor[1]}_series', f'{mentor[1]}_theme')


if __name__ == '__main__':
    pass
