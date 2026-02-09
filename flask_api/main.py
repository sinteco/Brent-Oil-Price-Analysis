from flask import Flask, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')

def load_csv(path):
    if os.path.exists(path):
        df = pd.read_csv(path)
        # Convert NaN to None for JSON compliance
        return df.fillna(np.nan).replace({np.nan: None})
    return None

@app.route('/api/historical', methods=['GET'])
def get_historical():
    path = os.path.join(DATA_DIR, 'processed', 'BrentOilPrices_cleaned.csv')
    df = load_csv(path)
    if df is not None:
        # Convert date to string for JSON serialization
        df['Date'] = df['Date'].astype(str)
        return jsonify(df.to_dict(orient='records'))
    return jsonify({"error": "Data not found"}), 404

@app.route('/api/events', methods=['GET'])
def get_events():
    path = os.path.join(DATA_DIR, 'external', 'major_events.csv')
    df = load_csv(path)
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({"error": "Events not found"}), 404

@app.route('/api/change-points', methods=['GET'])
def get_change_points():
    path = os.path.join(DATA_DIR, 'processed', 'detected_change_points.csv')
    df = load_csv(path)
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({"error": "Change points not found"}), 404

@app.route('/api/impact', methods=['GET'])
def get_impact():
    path = os.path.join(DATA_DIR, 'processed', 'market_impact_analysis.csv')
    df = load_csv(path)
    if df is not None:
        return jsonify(df.to_dict(orient='records'))
    return jsonify({"error": "Impact analysis not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, port=5001)
