import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm

# Black-Scholes call option pricing function
def black_scholes_call(S, K, T, r, sigma):
    d1 = (np.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    return S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)

# Define range for stock price (S0) and volatility (σ)
S0_range = np.linspace(80, 120, 20)  # Stock prices from 80 to 120
vol_range = np.linspace(0.1, 0.5, 20)  # Volatility from 0.1 to 0.5

# Compute option prices using the Black-Scholes model
data = np.array([[black_scholes_call(S, 110, 1, 0.05, sigma)  # K=110, T=1, r=5%
                  for S in S0_range] for sigma in vol_range])

# Convert to DataFrame for visualization
df = pd.DataFrame(data, index=np.round(vol_range, 2), columns=np.round(S0_range, 2))

# Set up the heatmap
plt.figure(figsize=(10, 8))
sns.heatmap(df, annot=False, cmap="coolwarm", cbar=True)

# Customize plot aesthetics
plt.xlabel("Stock Price (S0)", fontsize=12, color="white")
plt.ylabel("Volatility (σ)", fontsize=12, color="white")
plt.title("Black-Scholes Call Option Pricing Heatmap", fontsize=14, color="white")

# Set dark mode styling
plt.gca().patch.set_facecolor('none')  # Transparent background
plt.xticks(rotation=45, fontsize=10, color="white")
plt.yticks(fontsize=10, color="white")

# Show the plot
plt.show()
