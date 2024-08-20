from taipy.gui import State
from typing import List
import pandas as pd

class State(State):
    data: pd.DataFrame
    displayed_data: pd.DataFrame
    show_city_info_pane: bool
    selected_view: str
    selected_currency: str
    selected_dates: List[str]
    selected_prices: List[int]
    selected_city: str
    selected_product_line: str
    selected_branch: str
    rate_info: str = "Good"
    rate_price: str = "Good"
    open_dialog_review: bool = False
    selected_row_for_review: pd.DataFrame = None
    city_info_dict: dict
