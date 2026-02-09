import pandas as pd
import numpy as np
import os

def preprocess_data(input_path, output_path):
    """
    Cleans and preprocesses the Brent oil price dataset.
    """
    print(f"Reading data from {input_path}...")
    # Read CSV, setting observation_date as index
    df = pd.read_csv(input_path)
    
    # Rename columns for consistency
    df.columns = ['Date', 'Price']
    
    # Convert Date to datetime objects
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Set Date as index
    df.set_index('Date', inplace=True)
    
    # Convert Price to numeric, handling missing values
    # The original CSV has empty strings for some dates
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
    
    # Check for missing values
    missing_count = df['Price'].isna().sum()
    print(f"Found {missing_count} missing price values.")
    
    # Handle missing values: Forward fill then backward fill
    # This is appropriate for daily financial time series
    df['Price'] = df['Price'].ffill().bfill()
    
    # Ensure no more missing values
    if df['Price'].isna().any():
        print("Warning: Missing values still exist after filling.")
    
    # Save the cleaned data
    print(f"Saving cleaned data to {output_path}...")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    print("Preprocessing complete.")

if __name__ == "__main__":
    raw_data_path = "data/raw/BrentOilPrices.csv"
    processed_data_path = "data/processed/BrentOilPrices_cleaned.csv"
    preprocess_data(raw_data_path, processed_data_path)
