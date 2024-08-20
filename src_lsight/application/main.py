from taipy.gui import Gui
from pages.filter_page.filter_page import *



def on_init(state: State):
    # A function called when a used first connect to the application
    pass


def on_change(state: State, var_name: str, var_value):
    # A function called when a variable changes
    pass


# Define pages for the GUI
pages = {
    "/": "",
    "filter_page": filter_page,
    "review_page": review_page,
}


# Run the GUI application
if __name__ == "__main__":
    gui = Gui(pages=pages)
    city_info_partial = gui.add_partial(build_city_info_partial(displayed_data))
    gui.run(title="Sales Insights", dark_mode=False)
