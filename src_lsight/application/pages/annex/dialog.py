import json
from taipy.gui import notify
import taipy.gui.builder as tgb
from state_class import State

# Initialize state variables
selected_row_for_review = None  # Holds the data of the selected row for review
rate_info = "Good"  # Default value for rating the information
rate_price = "Good"  # Default value for rating the price
open_dialog_review = False  # Controls the visibility of the review dialog


# Function to handle the review submission
def send_review(state: State, id: str, payload: dict):
    # Check if the "Send" button was clicked (button index 1)
    if payload["args"][0] == 1:
        # Load existing reviews from the JSON file
        with open("data/reviews.json", "r", encoding="utf-8") as f:
            reviews = json.load(f)

        # Extract the invoice ID from the selected row
        invoice_id = str(state.selected_row_for_review["Invoice_ID"].values[0])

        # Update the reviews dictionary with the new ratings
        reviews[invoice_id] = {
            "rate_info": state.rate_info,
            "rate_price": state.rate_price,
        }

        # Save the updated reviews back to the JSON file
        with open("data/reviews.json", "w", encoding="utf-8") as f:
            json.dump(reviews, f, indent=4)

        notify(state, "s", "Review added")
    else:
        notify(state, "w", "Rate not applied")

    # Close the review dialog
    state.open_dialog_review = False


# Function to open the review dialog for the selected row
def open_review(state: State, var_name: str, payload: dict):
    # Get the index of the selected row
    index = payload["index"]

    # Copy the data from the state and select the specific row
    data = getattr(state, var_name).copy()
    state.selected_row_for_review = data.iloc[index].to_frame().T

    # Open the review dialog
    state.open_dialog_review = True


# Function to build the review dialog
def build_dialog():
    # Create a dialog for reviewing the selected row
    tgb.dialog(
        page="review_page",  # The page content to display in the dialog
        open="{open_dialog_review}",  # Control visibility with a state variable
        on_action=send_review,  # Function to handle actions (Cancel/Send)
        labels=["Cancel", "Send"],  # Labels for the dialog buttons
        width="500px",
        title="Review the selected row",
    )


# Build the review page content
with tgb.Page() as review_page:
    tgb.text("Rate info", mode="md")

    # Table displaying the selected row's data
    tgb.table("{selected_row_for_review}")

    # Dropdown selector for rating the information quality
    tgb.selector(
        value="{rate_info}",
        lov=["Good", "Bad"],  # Options for the selector
        dropdown=True,
        label="Rate info",  # Label for the selector
        class_name="fullwidth",  # Full-width styling for the dropdown (default in 4.0)
    )

    tgb.text("Rate price", mode="md")

    # Dropdown selector for rating the price
    tgb.selector(
        value="{rate_price}",
        lov=["Good", "Bad"],  # Options for the selector
        dropdown=True,
        label="Rate price",  # Label for the selector
        class_name="fullwidth",  # Full-width styling for the dropdown (default in 4.0)
    )
