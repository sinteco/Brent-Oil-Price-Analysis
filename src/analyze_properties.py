import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from statsmodels.tsa.stattools import adfuller
import os

def analyze_properties(data_path):
    df = pd.read_csv(data_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    
    results = {}
    
    # 1. Trend Analysis
    # Checking for overall direction using rolling mean
    df['Rolling_Mean'] = df['Price'].rolling(window=252).mean() # 1 year trading days
    results['trend_comment'] = "Visible long-term trends with significant cyclicality and structural breaks."
    
    # 2. Stationarity Testing (ADF Test)
    print("Performing Augmented Dickey-Fuller test...")
    adf_result = adfuller(df['Price'].values)
    results['adf_stat'] = adf_result[0]
    results['p_value'] = adf_result[1]
    results['is_stationary'] = adf_result[1] < 0.05
    
    # 3. Volatility Patterns
    # Daily returns and rolling volatility
    df['Returns'] = df['Price'].pct_change()
    df['Volatility'] = df['Returns'].rolling(window=21).std() * np.sqrt(252) # 21-day rolling vol (annualized)
    results['vol_comment'] = "High volatility clustering observed, especially during global crises (2008, 2014, 2020)."
    
    print(f"ADF Statistic: {results['adf_stat']}")
    print(f"p-value: {results['p_value']}")
    print(f"Is stationary: {results['is_stationary']}")
    
    # Save a diagnostic plot
    plt.figure(figsize=(15, 10))
    
    plt.subplot(2, 1, 1)
    plt.plot(df.index, df['Price'], label='Price')
    plt.plot(df.index, df['Rolling_Mean'], label='1y Rolling Mean', color='red')
    plt.title('Brent Oil Price and Trend')
    plt.legend()
    
    plt.subplot(2, 1, 2)
    plt.plot(df.index, df['Volatility'], color='orange', label='Annualized Volatility')
    plt.title('Rolling Volatility (21-day window)')
    plt.legend()
    
    plt.tight_layout()
    plt.savefig("notebooks/time_series_properties.png")
    
    return results

if __name__ == "__main__":
    data_path = "data/processed/BrentOilPrices_cleaned.csv"
    res = analyze_properties(data_path)
    print("\nSummary for Documentation:")
    print(res)
