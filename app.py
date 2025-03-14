import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

st.title("Black-Scholes Option Pricing Heatmap")

# User Inputs for Heatmap Range
min_S0 = st.number_input("Min Stock Price (S0)", value=80.0)
max_S0 = st.number_input("Max Stock Price (S0)", value=120.0)
min_vol = st.number_input("Min Volatility (σ)", value=0.1)
max_vol = st.number_input("Max Volatility (σ)", value=0.5)
grid_size = st.slider("Grid Size", min_value=10, max_value=50, value=25)  # Adjust granularity

# Generate the meshgrid
S0_range = np.linspace(min_S0, max_S0, grid_size)
vol_range = np.linspace(min_vol, max_vol, grid_size)
data = np.random.rand(grid_size, grid_size) * 30  # Placeholder for option pricing function

df = pd.DataFrame(data, index=np.round(vol_range, 2), columns=np.round(S0_range, 2))

# Plot Heatmap
fig, ax = plt.subplots(figsize=(8, 6))
fig.patch.set_alpha(0)  # Transparent background
ax.set_facecolor('none')  # Transparent axis background

sns.heatmap(df, cmap="coolwarm", annot=False, ax=ax)

# Make text white
ax.xaxis.label.set_color("white")
ax.yaxis.label.set_color("white")
ax.tick_params(colors="white")
ax.spines[:].set_color("white")

st.pyplot(fig)
