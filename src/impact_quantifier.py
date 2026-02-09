import pandas as pd
import numpy as np
import os

def quantify_impacts(data_path, cp_path, output_path):
    """
    Calculates shifts in mean price and volatility between detected regimes.
    """
    df = pd.read_csv(data_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    
    cp_df = pd.read_csv(cp_path, parse_dates=['Date'])
    change_points = sorted(cp_df['Date'].tolist())
    
    # Define regime boundaries
    regime_starts = [df.index.min()] + change_points
    regime_ends = change_points + [df.index.max()]
    
    impacts = []
    
    for i, (start, end) in enumerate(zip(regime_starts, regime_ends)):
        regime_data = df.loc[start:end]
        
        # Basic stats
        mean_price = regime_data['Price'].mean()
        volatility = regime_data['Price'].std()
        
        # Returns for better volatility comparison
        returns = regime_data['Price'].pct_change().dropna()
        ann_vol = returns.std() * np.sqrt(252) # Annualized daily return vol
        
        impacts.append({
            'Regime': i + 1,
            'Start_Date': start,
            'End_Date': end,
            'Mean_Price': mean_price,
            'Std_Dev': volatility,
            'Ann_Vol_Returns': ann_vol
        })
    
    results = pd.DataFrame(impacts)
    
    # Calculate deltas (%)
    results['Price_Change_Pct'] = results['Mean_Price'].pct_change() * 100
    results['Vol_Change_Pct'] = results['Ann_Vol_Returns'].pct_change() * 100
    
    print("Market Impact Summary:")
    print(results)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    results.to_csv(output_path, index=False)
    print(f"Impact analysis saved to {output_path}")

if __name__ == "__main__":
    data_path = "data/processed/BrentOilPrices_cleaned.csv"
    cp_path = "data/processed/detected_change_points.csv"
    output_path = "data/processed/market_impact_analysis.csv"
    
    if os.path.exists(cp_path):
        quantify_impacts(data_path, cp_path, output_path)
    else:
        print(f"Error: Change point file {cp_path} not found. Run model.py first.")
