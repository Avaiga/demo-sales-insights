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

# Load city information from a JSON file
with open("data/cities.json", "r", encoding="utf-8") as f:
    city_info_dict = json.load(f)


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
    # TODO: Nothing to do here, just look how my partial is being updated after a filter
    state.city_info_partial.update_content(state, build_city_info(state.displayed_data))


# Function to convert the total values based on the selected currency
def convert(state):
    if state.selected_currency == "USD":
        state.displayed_data["Total"] = state.displayed_data["Total ($)"]
    elif state.selected_currency == "EUR":
        state.displayed_data["Total"] = state.displayed_data["Total (€)"]
    state.refresh("displayed_data")


# Function to handle the review submission
def send_review(state, id, payload):
    if payload["args"][0] == 1:  # If the second button is clicked (Send)
        with open("data/reviews.json", "r", encoding="utf-8") as f:
            reviews = json.load(f)
        invoice_id = str(state.selected_row_for_review["Invoice_ID"][-1])
        reviews[invoice_id] = {
            "rate_info": state.rate_info,
            "rate_price": state.rate_price,
        }
        with open("data/reviews.json", "w", encoding="utf-8") as f:
            json.dump(reviews, f, indent=4)

        notify(state, "s", "Review added")
    else:
        notify(state, "w", "Rate not applied")

    state.open_dialog_review = False


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
        class_name="fullwidth",
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


# Function to handle the review process
def open_review(state, var_name: str, payload: dict):
    index = payload["index"]
    data = getattr(state, var_name).copy()
    state.selected_row_for_review = data.iloc[index].to_frame().T
    state.open_dialog_review = True


with tgb.Page() as review_page:
    tgb.text("Rate info", mode="md")
    tgb.table("{selected_row_for_review}")
    tgb.selector(
        value="{rate_info}",
        lov=["Good", "Bad"],
        dropdown=True,
        label="Rate info",
        class_name="fullwidth",  # native in 4.0
    )

    tgb.text("Rate price", mode="md")
    tgb.selector(
        value="{rate_price}",
        lov=["Good", "Bad"],
        dropdown=True,
        label="Rate price",
        class_name="fullwidth",  # native in 4.0
    )


# Build city information pane
def build_city_info(displayed_data):
    with tgb.Page() as page:
        tgb.text("### City Information", mode="md")
        # TODO: Create a page dynamically
        # Create an expandable for every unique city in the displayed_data
        # Each expandable should contain the city information (city_info_dict)
    return page


# Build the main GUI page
with tgb.Page() as page:
    with tgb.part(class_name="container"):
        tgb.text("Sales Insights", class_name="h1 text-center")

        with tgb.layout("1 1 1", gap="20px", columns__mobile="1"):
            with tgb.part():
                build_basic_filters()
            with tgb.part():
                build_conversion()

        tgb.html("hr")

        tgb.toggle(
            value="{selected_view}",
            lov=["Simple view", "Advanced view", "Raw view"],
        )

        with tgb.part(render="{selected_view=='Raw view'}"):
            tgb.table(
                "{data}",
                on_action=open_review,
                filter=True,
            )

        with tgb.part(render="{selected_view=='Simple view'}"):
            tgb.table(
                "{displayed_data}",
                columns=["Date", "City", "Product_line", "Total", "Review"],
                group_by__City=True,
                group_by__Product_line=True,
                apply_Total="mean",
                filter=True,
                on_action=open_review,
            )

        with tgb.part(render="{selected_view=='Advanced view'}"):
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
                on_action=open_review,
            )


        def open_pane(state):
            state.show_city_info_pane = True
        tgb.button(
            "City info",
            on_action=open_pane,
            id="open_pane",
        )

        # TODO: Create a pane that should open when show_city_info_pane is True,
        # and that contains the city_info_partial

        tgb.pane(
            open="{show_city_info_pane}",
            width="300px",
            anchor="right",
            partial="{city_info_partial}",
        )

        tgb.dialog(
            page="review_page",
            open="{open_dialog_review}",
            on_action=send_review,
            labels=["Cancel", "Send"],
            width="500px",
            title="Review the selected row",
        )


# Define pages for the GUI
pages = {"page": page, "review_page": review_page}

# Run the GUI application
if __name__ == "__main__":
    gui = Gui(pages=pages)
    # TODO: Nothing to do here, just look how my partial is being initialized
    city_info_partial = gui.add_partial(build_city_info(displayed_data))
    gui.run(title="Sales", port=2452)
