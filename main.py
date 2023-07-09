import dearpygui.dearpygui as dpg

from apps.graphs import make_graphs

dpg.create_context()


with dpg.font_registry():
    with dpg.font("fonts/Roboto-Light.ttf", 16) as default_font:
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic)


def main():
    with dpg.window(label='Main', tag='Main', no_close=True, no_collapse=True):
        dpg.bind_font(default_font)
        with dpg.tab_bar():
            with dpg.tab(label='График финансов'):
                make_graphs()

            with dpg.tab(label='Добавить ментора'):
                dpg.add_text(default_value='В разработке...')

            with dpg.tab(label='Добавить оплату'):
                dpg.add_text(default_value='В разработке...')

            with dpg.tab(label='Все менторы'):
                dpg.add_text(default_value='В разработке...')

            with dpg.tab(label='Все финансы'):
                dpg.add_text(default_value='В разработке...')


if __name__ == '__main__':
    dpg.create_viewport(title='Jannat BILIM', width=1280, height=720)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.maximize_viewport()
    main()
    dpg.set_primary_window('Main', True)
    dpg.start_dearpygui()
    dpg.destroy_context()
