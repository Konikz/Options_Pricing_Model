import numpy as np
from pymongo import MongoClient
from scipy.stats import norm
import datetime

# MongoDB Setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["options_pricing"]
collection = db["option_prices"]

def black_scholes(S, K, T, r, sigma):
    """Calculate Black-Scholes call and put option prices."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    call = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    put = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    
    return call, put, d1, d2

def compute_greeks(S, K, T, r, sigma):
    """Compute Black-Scholes Greeks."""
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    delta = norm.cdf(d1)
    gamma = norm.pdf(d1) / (S * sigma * np.sqrt(T))
    vega = S * norm.pdf(d1) * np.sqrt(T)
    theta = (-S * norm.pdf(d1) * sigma / (2 * np.sqrt(T))) - (r * K * np.exp(-r * T) * norm.cdf(d2))
    rho = K * T * np.exp(-r * T) * norm.cdf(d2)

    return delta, gamma, vega, theta, rho

if __name__ == "__main__":
    print("Welcome to the Black-Scholes Option Pricer")

    # Taking user inputs
    S0 = float(input("Enter Current Stock Price (S0): "))
    K = float(input("Enter Strike Price (K): "))
    T = float(input("Enter Time to Expiry in years (T): "))
    r = float(input("Enter Risk-Free Interest Rate as decimal (r): "))
    sigma = float(input("Enter Volatility as decimal (σ): "))

    # Compute option prices
    call, put, d1, d2 = black_scholes(S0, K, T, r, sigma)
    delta, gamma, vega, theta, rho = compute_greeks(S0, K, T, r, sigma)

    # Print the results
    print("\nCalculated Option Prices:")
    print(f"Call Option Price: {call:.2f}")
    print(f"Put Option Price: {put:.2f}")

    print("\nCalculated Greeks:")
    print(f"Delta: {delta:.4f}")
    print(f"Gamma: {gamma:.4f}")
    print(f"Vega: {vega:.4f}")
    print(f"Theta: {theta:.4f}")
    print(f"Rho: {rho:.4f}")

    # Store in MongoDB
    option_data = {
        "date": datetime.datetime.utcnow(),
        "S0": S0,
        "K": K,
        "T": T,
        "r": r,
        "sigma": sigma,
        "call_price": call,
        "put_price": put,
        "Delta": delta,
        "Gamma": gamma,
        "Vega": vega,
        "Theta": theta,
        "Rho": rho,
    }
    collection.insert_one(option_data)
    print("\n✅ Data successfully stored in MongoDB.")
