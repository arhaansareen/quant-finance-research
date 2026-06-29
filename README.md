# Quant Finance Research

Independent quantitative finance research using Python. Exploring market efficiency, volatility modeling, statistical properties of financial returns, and derivatives pricing.

## Research Areas
- Efficient Market Hypothesis testing
- Time series modelling (ARIMA, GARCH)
- Volatility analysis and forecasting
- Monte Carlo simulations
- Options pricing and derivatives

## Projects

### 1. EMH Statistical Analysis (`emh-analysis/`)
**Status:** Complete

Tests whether S&P 500 daily log returns follow a normal distribution — a core assumption of weak-form market efficiency.

**Methodology:**
- Downloaded S&P 500 historical data (2020–2024) via yfinance
- Calculated log returns and analyzed distribution properties
- Tested for normality, skewness, and excess kurtosis
- Compared empirical distribution against theoretical normal distribution

**Key Findings:**
- Skewness: -0.48 (negative tail — bad days are worse than good days are good)
- Kurtosis: 11.8 (vs 0 for a normal distribution — significant fat tails)
- Worst single day: -11.98% | Best single day: +9.38%
- Under a normal distribution these moves should be statistically near-impossible

**Conclusion:** S&P 500 returns exhibit significant excess kurtosis inconsistent with the random walk hypothesis, providing early evidence against weak-form EMH.

### 2. ARIMA Return Prediction (`arima-analysis/`)
**Status:** Complete

Tests whether an ARIMA time-series model can predict future S&P 500 returns from past returns — a direct test of weak-form market efficiency.

**Methodology:**
- S&P 500 log returns, 2015–2024 via yfinance
- Augmented Dickey-Fuller test to confirm stationarity
- ARIMA(1,0,1) fit on 80% train / 20% test split
- Compared forecast RMSE against a naive zero-forecast baseline

**Key Findings:**
- ARIMA RMSE: 0.012108 vs naive baseline 0.012107
- Improvement over naive forecast: -0.01% (effectively zero)
- The model captures no meaningful predictive signal from past returns

**Conclusion:** A standard time-series model cannot predict future returns from historical returns, providing direct empirical support for weak-form EMH — past prices do not inform future ones.
---

*More analyses added regularly. Each project builds toward a comprehensive test of market efficiency.*

## Tech Stack
Python 3 · pandas · numpy · scipy · matplotlib · plotly · statsmodels · arch · yfinance

## Roadmap
- [x] EMH statistical analysis + fat tails
- [x] ARIMA return prediction model
- [ ] GARCH volatility modelling
- [ ] Rolling window EMH testing
- [ ] Monte Carlo price simulations
- [ ] Black-Scholes options pricing
- [ ] Backtesting engine

## About
I'm a Grade 12 student interested in quantitative finance and computer science. This repo documents independent research into market efficiency and financial modeling.

Competing internationally in speedcubing (top 10 globally, 6x Canadian National Record holder) taught me to think about optimization and pattern recognition under pressure which the same lens I bring to analyzing financial markets.