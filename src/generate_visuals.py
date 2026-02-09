import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

def generate_final_plot():
    data_path = "data/processed/BrentOilPrices_cleaned.csv"
    df = pd.read_csv(data_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    
    # Filter for since 2012
    df_recent = df[df.index >= '2012-01-01']
    
    plt.figure(figsize=(15, 8))
    plt.plot(df_recent.index, df_recent['Price'], label='Brent Oil Price', color='blue', alpha=0.6)
    
    # Major events to highlight
    events_path = "data/external/major_events.csv"
    if os.path.exists(events_path):
        events_df = pd.read_csv(events_path)
        # Filter for relevant events in the plot range
        events_df['Date'] = pd.to_datetime(events_df['Date'])
        plot_events = events_df[events_df['Date'] >= df_recent.index.min()]
        
        for _, row in plot_events.iterrows():
            plt.axvline(row['Date'], color='red', linestyle='--', alpha=0.5)
            plt.text(row['Date'], df_recent['Price'].max() * 0.85, row['Event'], 
                     rotation=90, verticalalignment='top', fontsize=8, color='red')
    else:
        print("Warning: major_events.csv not found.")
        
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
