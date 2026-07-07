import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt

def black_scholes(S, K, T, r, sigma, option_type='call'):
    """
    Price a European option using the Black-Scholes formula.
    S: current stock price
    K: strike price
    T: time to expiration (years)
    r: risk-free interest rate (annual)
    sigma: volatility (annual)
    """
    d1 = (np.log(S / K) + (r + 0.5 * sigma**2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)

    if option_type == 'call':
        price = S * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    else:  # put
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)
    return price

# Example: price a call and put option
S = 100      # stock at $100
K = 100      # strike at $100 (at-the-money)
T = 1.0      # 1 year to expiry
r = 0.05     # 5% risk-free rate
sigma = 0.20 # 20% annual volatility

call = black_scholes(S, K, T, r, sigma, 'call')
put = black_scholes(S, K, T, r, sigma, 'put')

print("=== Black-Scholes Option Pricing ===")
print(f"Stock price: ${S}, Strike: ${K}, Expiry: {T}yr, Rate: {r:.0%}, Vol: {sigma:.0%}")
print(f"Call option price: ${call:.2f}")
print(f"Put option price:  ${put:.2f}")
print()

# Verify put-call parity: C - P = S - K*e^(-rT)
parity_lhs = call - put
parity_rhs = S - K * np.exp(-r * T)
print("=== Put-Call Parity Check ===")
print(f"C - P = {parity_lhs:.4f}")
print(f"S - K*e^(-rT) = {parity_rhs:.4f}")
print(f"Parity holds: {np.isclose(parity_lhs, parity_rhs)}")
print()

# Plot: how call price changes with stock price
stock_prices = np.linspace(50, 150, 100)
call_prices = [black_scholes(s, K, T, r, sigma, 'call') for s in stock_prices]
intrinsic = np.maximum(stock_prices - K, 0)  # value at expiry

plt.figure(figsize=(12, 6))
plt.plot(stock_prices, call_prices, label='Black-Scholes Call Price', linewidth=2, color='steelblue')
plt.plot(stock_prices, intrinsic, label='Intrinsic Value (at expiry)', linestyle='--', color='gray')
plt.axvline(K, color='red', linestyle=':', alpha=0.6, label='Strike Price')
plt.title('Black-Scholes Call Option Price vs Stock Price')
plt.xlabel('Stock Price ($)')
plt.ylabel('Option Price ($)')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig('black_scholes_curve.png', dpi=120)
plt.show()

print("Done - saved black_scholes_curve.png")
