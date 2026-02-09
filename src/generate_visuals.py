import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def generate_final_plot():
    data_path = "data/processed/BrentOilPrices_cleaned.csv"
    df = pd.read_csv(data_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    
    # Filter for since 2012
    df_recent = df[df.index >= '2012-01-01']
    
    plt.figure(figsize=(15, 8))
    plt.plot(df_recent.index, df_recent['Price'], label='Brent Oil Price', color='blue', alpha=0.6)
    
    # Major events to highlight
    events = [
        ('2014-06-01', 'Oil Price Crash (OPEC Policy Shift)'),
        ('2020-03-11', 'COVID-19 Pandemic Start'),
        ('2022-02-24', 'Russia-Ukraine War')
    ]
    
    for date, label in events:
        plt.axvline(pd.to_datetime(date), color='red', linestyle='--', alpha=0.8)
        plt.text(pd.to_datetime(date), df_recent['Price'].max() * 0.9, label, rotation=90, verticalalignment='top', fontsize=10, color='red')
        
    # Detected change points (from model)
    detected = ['2020-12-29', '2022-01-03']
    for date in detected:
        plt.axvline(pd.to_datetime(date), color='green', linestyle='-', alpha=0.5, linewidth=3)
        plt.text(pd.to_datetime(date), df_recent['Price'].min() * 1.5, 'Model Change Point', rotation=90, verticalalignment='bottom', fontsize=10, color='green')

    plt.title('Brent Oil Prices (2012-2026) with Key Events and Model Change Points')
    plt.xlabel('Date')
    plt.ylabel('Price (USD/barrel)')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig("notebooks/final_analysis.png")
    print("Final analysis plot saved to notebooks/final_analysis.png")

if __name__ == "__main__":
    generate_final_plot()
