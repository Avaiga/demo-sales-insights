from taipy.gui import Gui, notify
import pandas as pd
import plotly.express as px
import taipy.gui.builder as tgb
import json

# Load and prepare data
data = pd.read_csv("data/modified_supermarkt_sales_plus.csv")
data["Date"] = pd.to_datetime(data["Date"])
data["Review"] = ["[Review](Review)" for _ in range(len(data))]
data["Total ($)"] = data["Total"]
data["Total (€)"] = data["Total"] * 1.2
displayed_data = data.copy()

# Initialize state variables with default values
show_city_info_pane = True
selected_view = "Simple view"
selected_currency = "USD"
selected_dates = [data["Date"].min().date(), data["Date"].max().date()]
selected_prices = [0, 5000]
selected_city = "All"
selected_product_line = "All"
selected_branch = "All"
rate_info = "Good"
rate_price = "Good"
open_dialog_review = False
selected_row_for_review = None


# Function to filter the data based on selected criteria
def filter(state):
    filtered_data = state.data

    if state.selected_city != "All":
        filtered_data = filtered_data[filtered_data["City"] == state.selected_city]

    if state.selected_product_line != "All":
        filtered_data = filtered_data[
            filtered_data["Product_line"] == state.selected_product_line
        ]

    if state.selected_branch != "All":
        filtered_data = filtered_data[filtered_data["Branch"] == state.selected_branch]

    filtered_data = filtered_data[
        (filtered_data["Date"].dt.date >= state.selected_dates[0])
        & (filtered_data["Total"] >= state.selected_prices[0])
        & (filtered_data["Total"] <= state.selected_prices[1])
    ]

    state.displayed_data = filtered_data


# Function to convert the total values based on the selected currency
def convert(state):
    if state.selected_currency == "USD":
        state.displayed_data["Total"] = state.displayed_data["Total ($)"]
    elif state.selected_currency == "EUR":
        state.displayed_data["Total"] = state.displayed_data["Total (€)"]
    state.refresh("displayed_data")


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


# Build conversion section
def build_conversion():
    tgb.text("### Conversion", mode="md")
    tgb.selector(
        value="{selected_currency}",
        lov=["USD", "EUR"],
        dropdown=True,
        label="Currency",
        on_change=convert,
        class_name="fullwidth", # native in 4.0
    )

    tgb.text("Date Range")
    tgb.date_range(
        "{selected_dates}", label_start="Start", label_end="End", on_change=filter
    )

    tgb.text("Price Range")
    tgb.slider(
        "{selected_prices}",
        min=0,
        max=5000,
        on_change=filter,
        continuous=False,
        width="100%",
    )


# Build the main GUI page
with tgb.Page() as page:
    with tgb.part(class_name="container"):
        tgb.text("Sales Insights", class_name="h1 text-center")

        # TODO: add a layout block to have filters side by side
        build_basic_filters()

        build_conversion()

        tgb.html("hr")  # This created a divider

        tgb.toggle(
            value="{selected_view}",
            lov=["Simple view", "Advanced view", "Raw view"],
        )

        with tgb.part(render="{selected_view=='Raw View'}"):  # TODO: make render work
            tgb.table(
                "{data}",
                filter=True,
            )

        with tgb.part(render="{selected_view=='Simple view'}"):  # TODO: make render work
            tgb.table(
                "{displayed_data}",
                columns=["Date", "City", "Product_line", "Total", "Review"],
                group_by__City=True,
                group_by__Product_line=True,
                apply_Total="mean",
                filter=True,
            )

        with tgb.part(render="{selected_view=='Advanced view'}"):  # TODO: make render work
            tgb.table(
                "{displayed_data}",
                columns=[
                    "City",
                    "Product_line",
                    "Total",
                    "Quantity",
                    "Tax_5%",
                    "Total",
                    "Date",
                    "Review",
                ],
                filter=True,
            )


# Run the GUI application
if __name__ == "__main__":
    gui = Gui(page)
    gui.run(title="Sales", port=2452)
