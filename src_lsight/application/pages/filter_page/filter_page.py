from data.data import data
from pages.annex.pane import build_city_info_partial, build_pane
from pages.annex.dialog import open_review, build_dialog
import taipy.gui.builder as tgb
from state_class import State

# Load and prepare the data
# Make a copy of the original data for displaying filtered results
displayed_data = data.copy()

# Initialize state variables with default values
# These variables control the filters and the selected view in the GUI
selected_view = "Simple view"
selected_currency = "USD"
selected_dates = [data["Date"].min().date(), data["Date"].max().date()]
selected_prices = [0, 5000]
selected_city = "All"
selected_product_line = "All"
selected_branch = "All"


# Function to filter the data based on selected criteria
def filter(state: State):
    # Start with the unfiltered data
    filtered_data = state.data

    # Define the filters to apply, skipping "All" options
    filters = {
        "City": state.selected_city,
        "Product_line": state.selected_product_line,
        "Branch": state.selected_branch,
    }

    # Apply each filter conditionally
    for column, selected_value in filters.items():
        if selected_value != "All":
            filtered_data = filtered_data[filtered_data[column] == selected_value]

    # Apply the date and price range filters
    filtered_data = filtered_data[
        (filtered_data["Date"].dt.date >= state.selected_dates[0])
        & (filtered_data["Date"].dt.date <= state.selected_dates[1])
        & (filtered_data["Total"] >= state.selected_prices[0])
        & (filtered_data["Total"] <= state.selected_prices[1])
    ]

    # Update the displayed data in the state
    state.displayed_data = filtered_data

    # Update the city info partial content
    state.city_info_partial.update_content(
        state, build_city_info_partial(state.displayed_data)
    )


# Function to convert the total values based on the selected currency
def convert(state: State):
    # Convert the 'Total' column based on selected currency
    if state.selected_currency == "USD":
        state.displayed_data["Total"] = state.displayed_data["Total ($)"]
    elif state.selected_currency == "EUR":
        state.displayed_data["Total"] = state.displayed_data["Total (€)"]

    # Refresh the displayed data
    state.refresh("displayed_data")


# Function to build the basic filters section of the GUI
def build_basic_filters():
    tgb.text("### Basic **Filters**", mode="md")

    # Filter for Product Line
    tgb.selector(
        value="{selected_product_line}",
        lov=["All"] + data["Product_line"].unique().tolist(),
        dropdown=True,
        filter=True,
        label="Product Line",
        on_change=filter,
        class_name="fullwidth m-half",
    )

    # Filter for City
    tgb.selector(
        value="{selected_city}",
        lov=["All"] + data["City"].unique().tolist(),
        dropdown=True,
        filter=True,
        label="City",
        on_change=filter,
        class_name="fullwidth m-half",
    )

    # Filter for Branch
    tgb.selector(
        value="{selected_branch}",
        lov=["All"] + data["Branch"].unique().tolist(),
        dropdown=True,
        filter=True,
        label="Branch",
        on_change=filter,
        class_name="fullwidth m-half",
    )


# Function to build the currency conversion section of the GUI
def build_conversion():
    tgb.text("### Conversion", mode="md")

    # Currency selector
    tgb.selector(
        value="{selected_currency}",
        lov=["USD", "EUR"],
        dropdown=True,
        label="Currency",
        on_change=convert,
        class_name="fullwidth m-half",
    )

    # Date range selector
    tgb.text("Date Range")
    tgb.date_range(
        "{selected_dates}", label_start="Start", label_end="End", on_change=filter
    )

    # Price range slider
    tgb.text("Price Range")
    tgb.slider(
        "{selected_prices}",
        min=0,
        max=5000,
        on_change=filter,
        continuous=False,
        width="100%",
    )


# Function to build the main GUI page
with tgb.Page() as filter_page:
    # container is just a style element
    # d-flex serves to put the pane side by side with the page
    with tgb.part(class_name="container d-flex"):
        with tgb.part():
            tgb.text("# Sales **Insights**", mode="md", class_name="text-center")

            # Layout for basic filters and conversion sections
            with tgb.layout("1 1 1", gap="30px", columns__mobile="1"):
                with tgb.part():
                    build_basic_filters()
                with tgb.part():
                    build_conversion()

            tgb.html("hr")  # Horizontal line separator

            # Toggle for selecting the view type
            tgb.toggle(
                value="{selected_view}",
                lov=["Simple view", "Advanced view", "Raw view"],
            )

            tgb.html("br")

            # Raw view: displays the full dataset without filtering
            with tgb.part(render="{selected_view=='Raw view'}"):
                tgb.table(
                    "{data}",
                    on_action=open_review,
                    filter=True,
                )

            # Simple view: displays a summarized version of the filtered data
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

            # Advanced view: displays a detailed version of the filtered data
            with tgb.part(render="{selected_view=='Advanced view'}"):
                tgb.table(
                    "{displayed_data}",
                    columns=[
                        "City",
                        "Product_line",
                        "Total",
                        "Quantity",
                        "Tax_5%",
                        "Date",
                        "Review",
                    ],
                    group_by__City=True,
                    group_by__Product_line=True,
                    apply_Total="mean",
                    filter=True,
                    on_action=open_review,
                )

        # Button to open the city info pane
        def open_info_pane(state):
            state.show_city_info_pane = True

        tgb.button(
            "City info",
            on_action=open_info_pane,
            id="open_pane",
        )

        build_pane()

        build_dialog()
