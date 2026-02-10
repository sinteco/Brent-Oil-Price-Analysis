# Brent Oil Price Analysis

A comprehensive investigation into the structural dynamics of Brent Crude Oil pricing (1987–2026). This project combines Bayesian statistical modeling with interactive visualization to identify regime shifts and quantify the economic impact of major geopolitical and economic events.

## 🚀 Key Features

- **Bayesian Change Point Modeling**: PyMC-based detection of price regime shifts with full posterior uncertainty quantification for breakpoint locations, regime means, and volatility.
- **15 Validated Market Shock Events**: A curated chronology of conflicts, OPEC policy shifts, sanctions, and economic crises used as independent validation markers.
- **Robust Data Pipeline**: All scripts include input validation, convergence diagnostics (R-hat, ESS), and structured error handling.
- **Interactive Dashboards**:
  - **Streamlit**: Lightweight, data-centric dashboard for research exploration.
  - **Flask + React**: Full-stack analytical application with Recharts visualizations and event highlighting.

## 📁 Project Structure

```text
├── WORKFLOW.md             # Analysis workflow, assumptions & limitations
├── dashboard/              # Streamlit dashboard
├── flask_api/              # Flask Backend API
│   └── API_DOCS.md         # API endpoint documentation
├── react_ui/               # React Frontend (Vite + Recharts)
├── src/
│   ├── data_preprocessing.py   # Step 2: Cleaning & validation
│   ├── analyze_properties.py   # Step 3: EDA (ADF, volatility)
│   ├── generate_visuals.py     # Step 5: Event-annotated plots
│   ├── model.py                # Step 6: Bayesian Change Point model
│   ├── task2_model.py          # Task 2: Focused structural break model
│   └── impact_quantifier.py    # Regime impact quantification
├── notebooks/              # Generated plots & analysis artifacts
├── data/
│   ├── raw/                # Raw Brent prices (FRED)
│   ├── processed/          # Cleaned data & model results
│   └── external/           # Historical events dataset (15 events)
└── tests/                  # Unit tests
```

## 🛠️ Installation & Setup

### 1. Python Environment
```bash
pip install pymc arviz pandas matplotlib seaborn flask flask-cors statsmodels numpy
```

### 2. React Frontend
```bash
cd react_ui && npm install
```

## 🏃 Running the Project

### Analysis Pipeline (Sequential)
```bash
# Step 2: Preprocess raw data
python src/data_preprocessing.py

# Step 3: Run EDA (ADF test, volatility analysis)
python src/analyze_properties.py

# Step 6: Bayesian Change Point model
python src/model.py
```

### Interactive Dashboards

#### Streamlit (Lightweight)
```bash
streamlit run dashboard/app.py
```

#### Full-Stack (Flask + React)
```bash
# Terminal 1: Start Flask API (Port 5001)
python flask_api/main.py

# Terminal 2: Start React Dev Server (Port 3000)
cd react_ui && npm run dev
```

## 📊 Key Results

| Finding | Value |
|---------|-------|
| Detected Change Point | July 27, 2021 |
| Pre-Break Mean Price | $57.77 |
| Post-Break Mean Price | $92.52 |
| Net Price Increase | **+60.16%** |
| COVID-19 Volatility Spike | **+287%** |
| Post-Break Volatility Change | **-73%** |

## 📄 Documentation

- **[WORKFLOW.md](WORKFLOW.md)**: Detailed 6-step analysis workflow, 7 key assumptions, 5 known limitations, and expected model outputs.
- **[flask_api/API_DOCS.md](flask_api/API_DOCS.md)**: REST API endpoint reference.

## 🌿 Branch Overview

| Branch | Content |
|--------|---------|
| `main` | Final consolidated project state |
| `task1` | Data acquisition, EDA, event research, and workflow documentation |
| `task2` | Bayesian change point modeling and impact quantification |
| `task3` | Full-stack Flask + React dashboard implementation |
