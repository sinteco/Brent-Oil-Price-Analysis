# Brent Oil Price Analysis

This project analyzes historical Brent oil prices (1987-2022) to identify structural breaks and quantify the impact of significant geopolitical and economic events using Bayesian Statistical Modeling.

## 🚀 Key Features

- **Bayesian Change Point Modeling**: Using PyMC to detect shifts in price mean and volatility.
- **Structural Break Analysis**: Quantitative impact analysis of events like the 1990 Kuwait Invasion, 2008 Financial Crisis, and 2020 COVID-19 pandemic.
- **Interactive Dashboards**:
  - **Streamlit**: Fast, data-centric dashboard for research exploration.
  - **Flask + React**: Full-stack analytical application with interactive Recharts visualizations and event highlighting.

## 📁 Project Structure

```text
├── dashboard/              # Streamlit dashboard
├── flask_api/             # Flask Backend API
├── react_ui/              # React Frontend (Vite)
├── src/                   # Analysis & Modeling scripts
├── notebooks/             # Exploratory Data Analysis & Plots
├── data/
│   ├── raw/               # Raw Brent prices (FRED)
│   ├── processed/         # Cleaned data & model results
│   └── external/          # Historical events dataset
└── tests/                 # Unit tests
```

## 🛠️ Installation & Setup

### 1. Backend (Python)
```bash
# Install dependencies
pip install pymc arviz pandas matplotlib seaborn flask flask-cors
```

### 2. Frontend (React)
```bash
cd react_ui
npm install
```

## 🏃 Running the Project

### Analysis & Modeling
To run the Bayesian analysis:
```bash
python src/model.py
python src/impact_quantifier.py
```

### Interactive Dashboards

#### Streamlit (Lightweight)
```bash
streamlit run dashboard/app.py
```

#### Full-Stack (Flask + React)
```bash
# Start Flask API (Port 5001)
python flask_api/main.py

# In another terminal, start React Dev Server (Port 3000)
cd react_ui
npm run dev
```

## 📊 Results Summary
The analysis identified a massive 287% volatility spike and a 41% price drop during the 2020 COVID-19 regime. Recent structural breaks (July 2021) align with the global energy supply constraints, resulting in a 60% increase in average price levels.

## 🌿 Branch Overview
- `main`: Final project state.
- `task1`: Analysis foundation and data acquisition.
- `task2`: Bayesian change point modeling and impact quantification.
- `task3`: Full-stack dashboard implementation.
