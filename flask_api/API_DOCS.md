# Brent Oil Price Analysis API

RESTful API developed with Flask to serve energy market analytical results.

## Base URL
`http://localhost:5001`

## Endpoints

### 1. Get Historical Prices
- **URL**: `/api/historical`
- **Method**: `GET`
- **Description**: Returns all processed Brent oil prices.
- **Response**: List of `{ "Date": "YYYY-MM-DD", "Price": float }`

### 2. Get Historical Events
- **URL**: `/api/events`
- **Method**: `GET`
- **Description**: Returns significant political and economic events.
- **Response**: List of `{ "Date": "YYYY-MM-DD", "Event": string, "Category": string }`

### 3. Get Change Points
- **URL**: `/api/change-points`
- **Method**: `GET`
- **Description**: Returns structural breaks detected by the Bayesian model.
- **Response**: List of `{ "Date": "YYYY-MM-DD", "Change_Point_Index": float }`

### 4. Get Market Impact
- **URL**: `/api/impact`
- **Method**: `GET`
- **Description**: Returns quantified regime shifts (Price & Volatility deltas).
- **Response**: List of regime statistics.

## Setup
```bash
pip install flask flask-cors pandas numpy
python main.py
```
