"""
Brent Oil Price Data Preprocessing Pipeline
============================================
Workflow Step 1: Data Acquisition & Cleaning

This script ingests raw Brent Crude Oil spot price data from FRED
and produces a clean, analysis-ready CSV.

Assumptions:
    - Input CSV has exactly two columns: observation date and price.
    - Missing prices are represented as empty strings or NaN (common in FRED exports
      for weekends/holidays that still appear in the download).
    - Forward-fill followed by backward-fill is appropriate for daily financial data
      because market prices do not change on non-trading days.
    - The FRED dataset is the authoritative source; no manual adjustments are made.

Limitations:
    - Interpolation cannot recover "true" prices for extended market closures.
    - This script does not adjust for inflation or currency fluctuations.
"""

import pandas as pd
import numpy as np
import os
import sys
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


def validate_raw_data(df):
    """Run robustness checks on raw input data before processing."""
    errors = []

    if df.shape[1] < 2:
        errors.append(f"Expected at least 2 columns, found {df.shape[1]}.")

    if df.empty:
        errors.append("Input DataFrame is empty.")

    if errors:
        for e in errors:
            logger.error(e)
        raise ValueError("Raw data validation failed. See errors above.")

    logger.info(f"Raw data validation passed: {len(df)} rows, {df.shape[1]} columns.")


def validate_cleaned_data(df):
    """Run post-processing integrity checks."""
    issues = []

    missing = df['Price'].isna().sum()
    if missing > 0:
        issues.append(f"{missing} missing values remain after cleaning.")

    negative = (df['Price'] < 0).sum()
    if negative > 0:
        issues.append(f"{negative} negative prices detected (Brent should always be positive).")

    if not df.index.is_monotonic_increasing:
        issues.append("Date index is not monotonically increasing.")

    if issues:
        for issue in issues:
            logger.warning(f"DATA QUALITY WARNING: {issue}")
    else:
        logger.info("Post-processing validation passed: no missing values, no negatives, dates sorted.")

    return len(issues) == 0


def preprocess_data(input_path, output_path):
    """
    Clean and preprocess the Brent oil price dataset.

    Args:
        input_path (str): Path to raw CSV from FRED.
        output_path (str): Path to save the cleaned CSV.

    Returns:
        pd.DataFrame: The cleaned DataFrame.

    Raises:
        FileNotFoundError: If input_path does not exist.
        ValueError: If raw data fails validation.
    """
    # --- Guard: file existence ---
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    logger.info(f"Reading data from {input_path}...")

    try:
        df = pd.read_csv(input_path)
    except Exception as e:
        raise IOError(f"Failed to read CSV: {e}")

    validate_raw_data(df)

    # Standardize column names
    df.columns = ['Date', 'Price']

    # Parse dates with error handling
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    bad_dates = df['Date'].isna().sum()
    if bad_dates > 0:
        logger.warning(f"Dropped {bad_dates} rows with unparseable dates.")
        df = df.dropna(subset=['Date'])

    df.set_index('Date', inplace=True)

    # Convert price to numeric
    df['Price'] = pd.to_numeric(df['Price'], errors='coerce')

    missing_count = df['Price'].isna().sum()
    total_count = len(df)
    logger.info(f"Found {missing_count}/{total_count} missing price values ({missing_count/total_count*100:.1f}%).")

    # Forward-fill then backward-fill (assumption documented in module docstring)
    df['Price'] = df['Price'].ffill().bfill()

    # Post-processing validation
    validate_cleaned_data(df)

    # Save
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path)
    logger.info(f"Cleaned data saved to {output_path} ({len(df)} rows).")

    return df


if __name__ == "__main__":
    raw_data_path = "data/raw/BrentOilPrices.csv"
    processed_data_path = "data/processed/BrentOilPrices_cleaned.csv"

    try:
        preprocess_data(raw_data_path, processed_data_path)
    except (FileNotFoundError, ValueError, IOError) as e:
        logger.critical(f"Preprocessing failed: {e}")
        sys.exit(1)
