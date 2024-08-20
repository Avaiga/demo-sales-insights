import pandas as pd

PATH_TO_DATA = "data/modified_supermarkt_sales_plus.csv"


def get_data(path_to_data: str = PATH_TO_DATA) -> pd.DataFrame:
    data = pd.read_csv(path_to_data)
    data["Date"] = pd.to_datetime(data["Date"])
    data["Review"] = ["[Review](Review)" for _ in range(len(data))]
    data["Total ($)"] = data["Total"]
    data["Total (€)"] = data["Total"] * 1.2
    return data


data = get_data(path_to_data=PATH_TO_DATA)
