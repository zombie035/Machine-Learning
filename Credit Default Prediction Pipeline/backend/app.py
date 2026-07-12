"""
app.py — Flask REST API for Credit Card Default Prediction
"""

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import joblib
import pandas as pd
import numpy as np
import os

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)

# ── Load model on startup ────────────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

print(f"Loading model from {MODEL_PATH}...")
artifact = joblib.load(MODEL_PATH)
pipeline = artifact["pipeline"]
FEATURES = artifact["features"]
print("Model loaded successfully.")

# ── Serve frontend ───────────────────────────────────────────────────────────
@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")

# ── Health check ─────────────────────────────────────────────────────────────
@app.route("/health")
def health():
    return jsonify({"status": "ok", "model": "Logistic Regression", "features": FEATURES})

# ── Prediction endpoint ───────────────────────────────────────────────────────
@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        # Validate all required features are present
        missing = [f for f in FEATURES if f not in data]
        if missing:
            return jsonify({"error": f"Missing fields: {missing}"}), 400

        # Build input dataframe
        row = {f: [float(data[f])] for f in FEATURES}
        X = pd.DataFrame(row)

        # Run pipeline
        prediction = int(pipeline.predict(X)[0])
        probability = float(pipeline.predict_proba(X)[0][1])

        risk_level = (
            "Low"    if probability < 0.3 else
            "Medium" if probability < 0.6 else
            "High"
        )

        return jsonify({
            "prediction": prediction,
            "probability": round(probability, 4),
            "probability_pct": round(probability * 100, 1),
            "risk_level": risk_level,
            "label": "Will Default" if prediction == 1 else "Will NOT Default"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    print("Starting Flask server on http://localhost:5000")
    app.run(debug=True, port=5000)
