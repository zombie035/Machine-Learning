from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd

# Flask application instance
app = Flask(__name__)

# A global prediction pipeline is loaded once at startup (faster per request).
# Note: the model artifacts (model_pipeline.pkl) are expected to be located
# alongside this file when running the app.
# Load the trained pipeline + artifacts created during model export.

with open('model_pipeline.pkl', 'rb') as f:
    pipeline = pickle.load(f)

# Expected keys from export_model.py
model = pipeline['model']
le_self = pipeline['label_encoder_self_employed']
feature_names = pipeline['feature_names']

@app.route('/')
def index():
    """Render the main prediction page (HTML form)."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests coming from the frontend.

    Expects a JSON body with keys matching the training feature names.
    Returns a JSON response with the predicted approval status and
    (when available) the positive-class probability.
    """
    # Expect JSON payload from the frontend form
    data = request.json

    try:
        # Build a single-row DataFrame in the exact feature order used during training.
        row = {f: None for f in feature_names}

        for f in feature_names:
            if f not in data:
                return jsonify({'error': f'Missing field: {f}'}), 400
            row[f] = data[f]

        df = pd.DataFrame([row])

        # encode self_employed
        df['self_employed'] = le_self.transform(df['self_employed'].astype(str))

        # Ensure numeric types
        df = df.astype(float)

        pred = model.predict(df)[0]
        prob = None
        if hasattr(model, 'predict_proba'):
            prob = float(model.predict_proba(df)[0, 1])

        result = 'Approved' if int(pred) == 1 else 'Rejected'
        return jsonify({'prediction': result, 'probability': prob})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)