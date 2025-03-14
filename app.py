import streamlit as st
import pymongo
import pandas as pd

# MongoDB Setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["options_pricing"]
collection = db["option_prices"]

# Streamlit UI
st.set_page_config(page_title="Black-Scholes Option Pricing", layout="wide")
st.title("🔍 Query Stored Option Pricing Data")

# Fetch all stored records
records = list(collection.find({}, {"_id": 0}))  # Exclude MongoDB's internal ID

if records:
    df = pd.DataFrame(records)

    # Dropdown to select a record based on date or stock price
    selected_record = st.selectbox(
        "Select a past calculation:",
        df["date"].astype(str) + " | S0: " + df["S0"].astype(str),
    )

    # Extract data for the selected record
    selected_data = df[df["date"].astype(str) + " | S0: " + df["S0"].astype(str) == selected_record].iloc[0]

    # Display retrieved data
    st.json(selected_data.to_dict())

    # Plot Greeks evolution (if historical data is available)
    if "Delta" in df.columns:
        st.subheader("📈 Greeks Over Time")
        st.line_chart(df[["date", "Delta", "Gamma", "Vega", "Theta", "Rho"]].set_index("date"))

else:
    st.warning("No historical data found in MongoDB.")
