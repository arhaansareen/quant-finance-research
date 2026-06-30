import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Download S&P 500 data
sp500 = yf.download('^GSPC', start='2015-01-01', end='2024-01-01')
sp500['Log_Returns'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
sp500 = sp500.dropna()
returns = sp500['Log_Returns']

# Estimate drift (mean) and volatility (std) from historical returns
mu = returns.mean()
sigma = returns.std()
last_price = float(sp500['Close'].iloc[-1].item())

print("=== Simulation Inputs ===")
print(f"Starting price: {last_price:.2f}")
print(f"Daily drift (mu): {mu:.6f}")
print(f"Daily volatility (sigma): {sigma:.6f}")
print()

# Simulation parameters
n_simulations = 10000   # number of possible future paths
n_days = 252            # one trading year ahead

# Run the Monte Carlo simulation
# Each day's return is drawn randomly from a normal distribution
np.random.seed(42)
simulations = np.zeros((n_days, n_simulations))
simulations[0] = last_price

for day in range(1, n_days):
    # random shock for each simulation
    random_returns = np.random.normal(mu, sigma, n_simulations)
    simulations[day] = simulations[day - 1] * np.exp(random_returns)

# Analyze the final-day outcomes
final_prices = simulations[-1]
print("=== Simulated Outcomes After 1 Year (10,000 paths) ===")
print(f"Mean ending price: {final_prices.mean():.2f}")
print(f"Median ending price: {np.median(final_prices):.2f}")
print(f"5th percentile (bad case): {np.percentile(final_prices, 5):.2f}")
print(f"95th percentile (good case): {np.percentile(final_prices, 95):.2f}")
print(f"Probability of a loss: {(final_prices < last_price).mean() * 100:.1f}%")
print()

# Plot 1: a sample of simulated paths
plt.figure(figsize=(13, 6))
plt.plot(simulations[:, :200], linewidth=0.5, alpha=0.3)
plt.axhline(last_price, color='black', linestyle='--', linewidth=1, label='Starting price')
plt.title('Monte Carlo Simulation: 200 Possible S&P 500 Paths (1 Year)')
plt.xlabel('Trading Days Ahead')
plt.ylabel('Price')
plt.legend()
plt.tight_layout()
plt.savefig('monte_carlo_paths.png', dpi=120)
plt.show()

# Plot 2: distribution of final outcomes
plt.figure(figsize=(13, 5))
plt.hist(final_prices, bins=80, color='steelblue', alpha=0.7, edgecolor='white', linewidth=0.3)
plt.axvline(last_price, color='black', linestyle='--', label='Starting price')
plt.axvline(np.percentile(final_prices, 5), color='red', linestyle='--', label='5th percentile')
plt.axvline(np.percentile(final_prices, 95), color='green', linestyle='--', label='95th percentile')
plt.title('Distribution of Simulated Ending Prices After 1 Year')
plt.xlabel('Ending Price')
plt.ylabel('Frequency')
plt.legend()
plt.tight_layout()
plt.savefig('monte_carlo_distribution.png', dpi=120)
plt.show()

print("Done - saved monte_carlo_paths.png and monte_carlo_distribution.png")
