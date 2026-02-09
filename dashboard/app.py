import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

st.set_page_config(page_title="Brent Oil Price Analysis", layout="wide")

st.title("🛢️ Brent Oil Price Analysis & Event Impact")
st.markdown("""
This dashboard provides insights into historical Brent oil prices and the impact of significant political and economic events.
""")

# Load data
@st.cache_data
def load_data():
    data_path = "data/processed/BrentOilPrices_cleaned.csv"
    df = pd.read_csv(data_path, parse_dates=['Date'])
    df.set_index('Date', inplace=True)
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("Filter Data")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(df.index.min().date(), df.index.max().date()),
    min_value=df.index.min().date(),
    max_value=df.index.max().date()
)

filtered_df = df.loc[str(date_range[0]):str(date_range[1])]

# Main Price Chart
st.subheader("Historical Price Trend")
fig, ax = plt.subplots(figsize=(15, 6))
ax.plot(filtered_df.index, filtered_df['Price'], color='#1f77b4', linewidth=2)
ax.set_ylabel("Price (USD/barrel)")
ax.set_xlabel("Date")
ax.grid(True, linestyle='--', alpha=0.7)
st.pyplot(fig)

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${filtered_df['Price'].iloc[-1]:.2f}")
col2.metric("Max Price", f"${filtered_df['Price'].max():.2f}")
col3.metric("Min Price", f"${filtered_df['Price'].min():.2f}")

# Events Section
st.subheader("Significant Market Events")

@st.cache_data
def load_events():
    events_path = "data/external/major_events.csv"
    if os.path.exists(events_path):
        return pd.read_csv(events_path)
    return pd.DataFrame(columns=["Date", "Event", "Category"])

events_df = load_events()
st.dataframe(events_df, use_container_width=True)

# Model Insights
st.subheader("Statistical Model Insights")
st.info("The Bayesian Change Point model detects shifts in price regimes. Below are the detected change points for the 2018-2022 period.")
st.image("notebooks/model_trace_multi.png")
