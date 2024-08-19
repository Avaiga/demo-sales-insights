from taipy.gui import Gui
import pandas as pd
import taipy.gui.builder as tgb


# Load and prepare data
data = pd.read_csv("data/modified_supermarkt_sales_plus.csv")
data["Date"] = pd.to_datetime(data["Date"])
data["Review"] = ["[Review](Review)" for _ in range(len(data))]
data["Total ($)"] = data["Total"]
data["Total (€)"] = data["Total"] * 1.2
displayed_data = data.copy()


selected_city = "All"
selected_product_line = "All"
selected_branch = "All"


# Function to filter the data based on selected criteria
def filter(state):
    # TODO: Filter the data based on selected criteria (Product_line, City, Branch)
    # The dataframe that should be displayed is state.displayed_data
    # This is this dataframe that should be filtered depending on the selected criteria
    # It should be filtered from the original data (state.data)
    pass


# Build basic filters section
def build_basic_filters():
    tgb.text("### Basic Filters", mode="md")
    tgb.selector(
        value="{selected_product_line}",
        lov=["All"] + data["Product_line"].unique().tolist(),
        dropdown=True,
        filter=True,
        label="Product Line",
        on_change=filter,
        class_name="fullwidth",
    )
    tgb.selector(
        value="{selected_city}",
        lov=["All"] + data["City"].unique().tolist(),
        dropdown=True,
        filter=True,
        label="City",
        on_change=filter,
        class_name="fullwidth",
    )
    tgb.selector(
        value="{selected_branch}",
        lov=["All"] + data["Branch"].unique().tolist(),
        dropdown=True,
        filter=True,
        label="Branch",
        on_change=filter,
        class_name="fullwidth",
    )
    return page


# Build the main GUI page
with tgb.Page() as page:
    with tgb.part(class_name="container"):
        tgb.text("Sales Insights", class_name="h1 text-center")

        build_basic_filters()

        tgb.html("hr")

        tgb.table(
            "{displayed_data}",
            columns=["Date", "City", "Product_line", "Total", "Review"],
            group_by__City=True,
            group_by__Product_line=True,
            apply_Total="mean",
            filter=True,
        )


# Run the GUI application
if __name__ == "__main__":
    gui = Gui(page)
    gui.run(title="Sales", port=2452)
