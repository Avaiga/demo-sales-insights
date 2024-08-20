import json
import pandas as pd
import taipy.gui.builder as tgb

# Initialize the state variable to control the visibility of the city info pane
show_city_info_pane = True

# Load city information from a JSON file
# This dictionary will hold city information for display in the GUI
with open("data/cities.json", "r", encoding="utf-8") as f:
    city_info_dict = json.load(f)

# Function to build the city information pane
def build_pane():
    # Create a side pane that opens from the right when `show_city_info_pane` is True
    with tgb.pane(
        open="{show_city_info_pane}",
        width="300px",
        persistent=True,
        anchor="right",
    ):
        # Include a part to dynamically load city information
        tgb.part(partial="{city_info_partial}")

# Function to build the partial content for city information
def build_city_info_partial(displayed_data: pd.DataFrame):
    # Create a new page for the city information section
    with tgb.Page() as page:
        tgb.text("### City Information", mode="md")
        
        # Loop through each unique city in the filtered dataset
        for city in displayed_data["City"].unique():
            # Create an expandable section for each city
            with tgb.expandable(title=city, expanded=False):
                # Display the city information or a default message if none is available
                tgb.text(
                    city_info_dict.get(city, "No information available."), mode="md"
                )
    
    # Return the constructed page for use in the pane
    return page
