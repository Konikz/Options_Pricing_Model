import math
import streamlit as st
from scipy.stats import norm

# Function to calculate Black-Scholes Call and Put prices
def black_scholes(S0, K, T, r, sigma):
    d1 = (math.log(S0 / K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    call_price = S0 * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

    return round(call_price, 2), round(put_price, 2)

# Streamlit UI
st.title("📈 Black-Scholes Option Pricing Model")

# User Inputs
S0 = st.number_input("Current Stock Price (S0)", min_value=1.0, value=100.0)
K = st.number_input("Strike Price (K)", min_value=1.0, value=110.0)
T = st.slider("Time to Expiry (Years)", 0.01, 5.0, 1.0)
r = st.slider("Risk-Free Interest Rate (as decimal)", 0.0, 0.2, 0.05)
sigma = st.slider("Volatility (σ)", 0.01, 1.0, 0.2)

# Compute option prices
call, put = black_scholes(S0, K, T, r, sigma)

# Display results
st.write("### 📊 Option Prices")
st.success(f"💰 Call Option Price: **${call}**")
st.error(f"📉 Put Option Price: **${put}**")
