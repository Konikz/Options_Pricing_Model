import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma):
    """Computes Black-Scholes Call & Put option prices"""
    d1 = (np.log(S/K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call_price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put_price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

    return call_price, put_price

# Streamlit UI
st.title("Black-Scholes Option Pricing Heatmap")

# User Inputs
min_S0 = st.number_input("Min Stock Price (S0)", value=80.0)
max_S0 = st.number_input("Max Stock Price (S0)", value=120.0)
min_sigma = st.number_input("Min Volatility (σ)", value=0.10)
max_sigma = st.number_input("Max Volatility (σ)", value=0.50)
grid_size = st.slider("Grid Size", min_value=10, max_value=50, value=30)

# Dropdown to choose between Call and Put
option_type = st.selectbox("Select Option Type", ["Call", "Put"])

# Generate data grid
stock_prices = np.linspace(min_S0, max_S0, grid_size)
volatilities = np.linspace(min_sigma, max_sigma, grid_size)

heatmap_data = np.zeros((grid_size, grid_size))

for i, S0 in enumerate(stock_prices):
    for j, sigma in enumerate(volatilities):
        call_price, put_price = black_scholes(S0, 100, 1, 0.05, sigma)  # Strike = 100, T=1, r=5%
        heatmap_data[j, i] = call_price if option_type == "Call" else put_price

# Plot the heatmap
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(heatmap_data, xticklabels=np.round(stock_prices, 2), 
            yticklabels=np.round(volatilities, 2), cmap="coolwarm", ax=ax)

st.pyplot(fig)
