import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Download S&P 500 data
sp500 = yf.download('^GSPC', start='2020-01-01', end='2024-01-01')

# Calculate log returns
sp500['Log_Returns'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
sp500 = sp500.dropna()

# Basic statistics
returns = sp500['Log_Returns']
print(f"Mean daily return: {returns.mean():.6f}")
print(f"Std deviation: {returns.std():.6f}")
print(f"Skewness: {returns.skew():.4f}")
print(f"Kurtosis: {returns.kurtosis():.4f}")
print(f"Best day: {returns.max():.4f}")
print(f"Worst day: {returns.min():.4f}")

# Plot returns distribution vs normal
plt.figure(figsize=(12,5))
plt.hist(returns, bins=100, density=True, alpha=0.7, label='Log Returns')
x = np.linspace(returns.min(), returns.max(), 100)
plt.plot(x, stats.norm.pdf(x, returns.mean(), returns.std()), 
         'r-', linewidth=2, label='Normal Distribution')
plt.title('S&P 500 Log Returns vs Normal Distribution')
plt.xlabel('Log Return')
plt.ylabel('Frequency')
plt.legend()
plt.savefig('returns_distribution.png')
plt.show()

print("Done")