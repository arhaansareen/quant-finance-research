import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error

# Download S&P 500 data
sp500 = yf.download('^GSPC', start='2015-01-01', end='2024-01-01')
sp500['Log_Returns'] = np.log(sp500['Close'] / sp500['Close'].shift(1))
sp500 = sp500.dropna()
returns = sp500['Log_Returns']

# Stationarity test (ADF)
adf_result = adfuller(returns)
print("=== Augmented Dickey-Fuller Test ===")
print(f"ADF Statistic: {adf_result[0]:.4f}")
print(f"p-value: {adf_result[1]:.6f}")
print(f"Stationary: {'Yes' if adf_result[1] < 0.05 else 'No'}")
print()

# Train/test split
split = int(len(returns) * 0.8)
train, test = returns[:split], returns[split:]

# Fit ARIMA model
model = ARIMA(train, order=(1, 0, 1))
fitted = model.fit()
print("=== ARIMA(1,0,1) Model Summary ===")
print(fitted.summary().tables[1])
print()

# Forecast and evaluate
forecast = fitted.forecast(steps=len(test))
rmse = np.sqrt(mean_squared_error(test, forecast))
naive_rmse = np.sqrt(mean_squared_error(test, np.zeros(len(test))))

print("=== Predictive Performance ===")
print(f"ARIMA RMSE:        {rmse:.6f}")
print(f"Naive (zero) RMSE: {naive_rmse:.6f}")
print(f"Improvement over naive: {((naive_rmse - rmse) / naive_rmse * 100):.2f}%")
print()

# EMH interpretation
print("=== EMH Interpretation ===")
if abs(rmse - naive_rmse) / naive_rmse < 0.01:
    print("ARIMA barely beats a naive zero-forecast - consistent with weak-form EMH:")
    print("past returns carry almost no predictive information about future returns.")
else:
    print("ARIMA shows some predictive edge - potential weak-form inefficiency to investigate.")

# Plot actual vs predicted
plt.figure(figsize=(13, 5))
plt.plot(test.index, test.values, label='Actual Returns', alpha=0.6, linewidth=0.8)
plt.plot(test.index, forecast.values, label='ARIMA Forecast', color='red', linewidth=1.2)
plt.title('ARIMA(1,0,1) Forecast vs Actual S&P 500 Log Returns')
plt.xlabel('Date')
plt.ylabel('Log Return')
plt.legend()
plt.tight_layout()
plt.savefig('arima_forecast.png', dpi=120)
plt.show()

print("\nDone - saved arima_forecast.png")
