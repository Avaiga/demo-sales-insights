import pandas as pd

# Load and prepare data
data = pd.read_csv("data/modified_supermarkt_sales_plus.csv")
data["Date"] = pd.to_datetime(data["Date"])
data["Review"] = ["[Review](Review)" for _ in range(len(data))]
data["Total ($)"] = data["Total"]
data["Total (€)"] = data["Total"] * 1.2

# TODO: print the data and try to familiarize yourself with it
