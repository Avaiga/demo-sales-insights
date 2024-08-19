from taipy.gui import Gui
import pandas as pd
import taipy.gui.builder as tgb
from state_class import State

# Load and prepare data
data = pd.read_csv("data/modified_supermarkt_sales_plus.csv")
data["Date"] = pd.to_datetime(data["Date"])
data["Review"] = ["[Review](Review)" for _ in range(len(data))]
data["Total ($)"] = data["Total"]
data["Total (€)"] = data["Total"] * 1.2

# TODO:  1 - Create a page and add a table visual element
## You can add filter=True

# TODO: 2 - Add to this page selectors with some initial value and a list of values
## They will not filter anything at the moment
## You can do it for Product_line, City, Branch
## You can add dropdown=True


# Run the GUI application
if __name__ == "__main__":
    gui = Gui(page)
    gui.run(title="Sales", port=2452)
