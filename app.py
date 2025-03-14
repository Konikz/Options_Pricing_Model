import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Black-Scholes formula
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

def black_scholes_put(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)

# Streamlit UI
st.set_page_config(page_title="Black-Scholes Option Pricing", layout="wide")

st.title("Black-Scholes Option Pricing")

# User input section
col1, col2 = st.columns(2)

with col1:
    min_S = st.number_input("Min Stock Price ($S_0$)", min_value=1.0, value=80.0, step=1.0)
    max_S = st.number_input("Max Stock Price ($S_0$)", min_value=min_S + 1, value=120.0, step=1.0)
    strike_price = st.number_input("Strike Price ($K$)", min_value=1.0, value=100.0, step=1.0)

with col2:
    min_sigma = st.number_input("Min Volatility (σ)", min_value=0.01, value=0.10, step=0.01)
    max_sigma = st.number_input("Max Volatility (σ)", min_value=min_sigma + 0.01, value=0.50, step=0.01)
    risk_free_rate = st.number_input("Risk-Free Interest Rate (r)", min_value=0.0, value=0.05, step=0.01)
    time_to_expiry = st.number_input("Time to Expiry (T in years)", min_value=0.01, value=1.0, step=0.01)

# Grid Size Slider
grid_size = st.slider("Grid Size", min_value=10, max_value=50, value=30, step=1)

# Option Type Selection
heatmap_type = st.radio("Select Heatmap Type:", ("Call Option Price", "PnL Heatmap"))

# Generate data grid
S_values = np.linspace(min_S, max_S, grid_size)
sigma_values = np.linspace(min_sigma, max_sigma, grid_size)
call_prices = np.zeros((grid_size, grid_size))
pnl_values = np.zeros((grid_size, grid_size))

# Compute Call Prices and PnL
initial_call_price = black_scholes_call(strike_price, strike_price, time_to_expiry, risk_free_rate, (min_sigma + max_sigma) / 2)

for i, S in enumerate(S_values):
    for j, sigma in enumerate(sigma_values):
        call_prices[j, i] = black_scholes_call(S, strike_price, time_to_expiry, risk_free_rate, sigma)
        pnl_values[j, i] = call_prices[j, i] - initial_call_price  # Profit/Loss calculation

# Plot Heatmap
fig, ax = plt.subplots(figsize=(8, 6))

if heatmap_type == "Call Option Price":
    data = call_prices
    title = "Call Option Price Heatmap"
    cmap = "coolwarm"
else:
    data = pnl_values
    title = "PnL Heatmap"
    cmap = "RdYlGn"  # Green for gains, Red for losses

sns.heatmap(data, xticklabels=np.round(S_values, 2), yticklabels=np.round(sigma_values, 2), cmap=cmap, cbar=True, ax=ax)
ax.set_xlabel("Stock Price ($S_0$)")
ax.set_ylabel("Volatility (σ)")
ax.set_title(title)
plt.xticks(rotation=45)
plt.yticks(rotation=0)

# Show heatmap
st.pyplot(fig)
