import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
from pymongo import MongoClient
import datetime

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["option_pricing_db"]
collection = db["option_data"]

# Black-Scholes Formula
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Greeks Calculation
def black_scholes_greeks(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) - (r * K * np.exp(-r * T) * norm.cdf(d2))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    rho = K * T * np.exp(-r * T) * norm.cdf(d2)
    
    return delta, gamma, theta, vega, rho

# Streamlit UI
st.set_page_config(page_title="Black-Scholes Greeks & Option Pricing", layout="wide")
st.title("📊 Black-Scholes Option Pricing & Greeks with Database")

# User Inputs
col1, col2 = st.columns(2)
with col1:
    min_S = st.number_input("Min Stock Price ($S_0$)", min_value=1.0, value=80.0)
    max_S = st.number_input("Max Stock Price ($S_0$)", min_value=min_S + 1, value=120.0)
    strike_price = st.number_input("Strike Price ($K$)", min_value=1.0, value=100.0)

with col2:
    min_sigma = st.number_input("Min Volatility (σ)", min_value=0.01, value=0.10)
    max_sigma = st.number_input("Max Volatility (σ)", min_value=min_sigma + 0.01, value=0.50)
    risk_free_rate = st.number_input("Risk-Free Interest Rate (r)", min_value=0.0, value=0.05)
    time_to_expiry = st.number_input("Time to Expiry (T in years)", min_value=0.01, value=1.0)

grid_size = st.slider("Grid Size", min_value=10, max_value=50, value=30)
heatmap_type = st.radio("Select Heatmap Type:", ("Call Option Price", "PnL Heatmap", "Delta", "Gamma", "Theta", "Vega", "Rho"))

# Generate Data Grid
S_values = np.linspace(min_S, max_S, grid_size)
sigma_values = np.linspace(min_sigma, max_sigma, grid_size)
call_prices = np.zeros((grid_size, grid_size))
pnl_values = np.zeros((grid_size, grid_size))
greeks = np.zeros((grid_size, grid_size))

initial_call_price = black_scholes_call(strike_price, strike_price, time_to_expiry, risk_free_rate, (min_sigma + max_sigma) / 2)

for i, S in enumerate(S_values):
    for j, sigma in enumerate(sigma_values):
        call_prices[j, i] = black_scholes_call(S, strike_price, time_to_expiry, risk_free_rate, sigma)
        pnl_values[j, i] = call_prices[j, i] - initial_call_price
        delta, gamma, theta, vega, rho = black_scholes_greeks(S, strike_price, time_to_expiry, risk_free_rate, sigma)

        if heatmap_type == "Delta":
            greeks[j, i] = delta
        elif heatmap_type == "Gamma":
            greeks[j, i] = gamma
        elif heatmap_type == "Theta":
            greeks[j, i] = theta
        elif heatmap_type == "Vega":
            greeks[j, i] = vega
        elif heatmap_type == "Rho":
            greeks[j, i] = rho

# Store Data in MongoDB
record = {
    "timestamp": datetime.datetime.utcnow(),
    "S_range": [min_S, max_S],
    "sigma_range": [min_sigma, max_sigma],
    "strike_price": strike_price,
    "risk_free_rate": risk_free_rate,
    "time_to_expiry": time_to_expiry,
    "grid_size": grid_size,
    "heatmap_type": heatmap_type,
    "call_prices": call_prices.tolist(),
    "pnl_values": pnl_values.tolist(),
    "greeks": greeks.tolist(),
}
collection.insert_one(record)
st.success("✅ Data saved to database!")

# Plot Heatmap
fig, ax = plt.subplots(figsize=(9, 6))
if heatmap_type == "Call Option Price":
    data = call_prices
    title = "Call Option Price Heatmap"
    cmap = "coolwarm"
elif heatmap_type == "PnL Heatmap":
    data = pnl_values
    title = "PnL Heatmap"
    cmap = "RdYlGn"
else:
    data = greeks
    title = f"{heatmap_type} Heatmap"
    cmap = "viridis"

sns.heatmap(data, xticklabels=np.round(S_values, 1), yticklabels=np.round(sigma_values, 2), cmap=cmap, cbar=True, ax=ax, annot=False, fmt=".2f")
ax.set_xlabel("Stock Price ($S_0$)", fontsize=12)
ax.set_ylabel("Volatility (σ)", fontsize=12)
ax.set_title(title, fontsize=14)
plt.xticks(rotation=45)
plt.yticks(rotation=0)

st.pyplot(fig)

# Fetch & Display Past Records
st.subheader("📜 Past Stored Option Data")
past_data = list(collection.find().sort("timestamp", -1).limit(5))
for record in past_data:
    st.write(f"📌 **Date:** {record['timestamp']} | **Strike Price:** {record['strike_price']} | **Heatmap:** {record['heatmap_type']}")
