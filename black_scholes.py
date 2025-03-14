import math
from scipy.stats import norm

def black_scholes(S0, K, T, r, sigma):
    """
    Computes the Black-Scholes price for a European call and put option.

    Parameters:
    S0 (float)  : Current stock price
    K (float)   : Strike price
    T (float)   : Time to expiry (in years)
    r (float)   : Risk-free interest rate (as a decimal)
    sigma (float): Volatility of the stock (as a decimal)

    Returns:
    tuple: (Call price, Put price)
    """
    d1 = (math.log(S0 / K) + (r + (sigma ** 2) / 2) * T) / (sigma * math.sqrt(T))
    d2 = d1 - sigma * math.sqrt(T)

    call_price = S0 * norm.cdf(d1) - K * math.exp(-r * T) * norm.cdf(d2)
    put_price = K * math.exp(-r * T) * norm.cdf(-d2) - S0 * norm.cdf(-d1)

    return round(call_price, 2), round(put_price, 2)

if __name__ == "__main__":
    print("Welcome to the Black-Scholes Option Pricer")
    
    # Taking user inputs
    S0 = float(input("Enter Current Stock Price (S0): "))
    K = float(input("Enter Strike Price (K): "))
    T = float(input("Enter Time to Expiry in years (T): "))
    r = float(input("Enter Risk-Free Interest Rate as decimal (r): "))
    sigma = float(input("Enter Volatility as decimal (σ): "))

    # Compute option prices
    call, put = black_scholes(S0, K, T, r, sigma)

    # Print the results
    print("\nCalculated Option Prices:")
    print(f"Call Option Price: {call}")
    print(f"Put Option Price: {put}")
