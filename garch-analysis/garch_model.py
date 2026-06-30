import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from arch import arch_model

# Download S&P 500 data
sp500 = yf.download('^GSPC', start='2015-01-01', end='2024-01-01')
sp500['Log_Returns'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
sp500 = sp500.dropna()

# arch library works best with returns scaled to percentage points
returns = sp500['Log_Returns'] * 100

# Fit a GARCH(1,1) model
# vol='Garch', p=1 (lag of past volatility), q=1 (lag of past shocks)
model = arch_model(returns, vol='Garch', p=1, q=1, dist='normal')
fitted = model.fit(disp='off')

print("=== GARCH(1,1) Model Summary ===")
print(fitted.summary())
print()

# Extract the key parameters
params = fitted.params
print("=== Key Parameters ===")
print(f"omega (baseline variance): {params['omega']:.6f}")
print(f"alpha[1] (reaction to shocks): {params['alpha[1]']:.4f}")
print(f"beta[1] (volatility persistence): {params['beta[1]']:.4f}")
print(f"alpha + beta (total persistence): {params['alpha[1]'] + params['beta[1]']:.4f}")
print()

# Interpretation
persistence = params['alpha[1]'] + params['beta[1]']
print("=== Interpretation ===")
print(f"Volatility persistence (alpha+beta) = {persistence:.4f}")
if persistence > 0.9:
    print("High persistence (>0.9): volatility shocks decay slowly.")
    print("This is volatility clustering — calm periods and turbulent periods")
    print("both tend to persist. A core stylized fact of financial markets.")
print()

# Plot conditional volatility vs returns
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), sharex=True)

ax1.plot(returns.index, returns.values, linewidth=0.6, color='steelblue')
ax1.set_title('S&P 500 Daily Log Returns (%)')
ax1.set_ylabel('Return (%)')

ax2.plot(sp500.index, fitted.conditional_volatility, linewidth=1, color='crimson')
ax2.set_title('GARCH(1,1) Estimated Conditional Volatility')
ax2.set_ylabel('Volatility (%)')
ax2.set_xlabel('Date')

plt.tight_layout()
plt.savefig('garch_volatilitpng', dpi=120)
plt.show()

print("Done - saved garch_volatility.png")
