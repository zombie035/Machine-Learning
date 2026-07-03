# Loan Approval Web App

Simple Flask web app that serves a prediction form for loan approval using a Gradient Boosting model.

Quick start:

1. Create a Python environment and install dependencies:

```bash
pip install -r requirements.txt
```

2. Train and export the model (this reads `loan_approval_dataset.csv`):

```bash
python export_model.py
```

This produces `model_pipeline.pkl`.

3. Run the Flask app:

```bash
python app.py
```

4. Open http://127.0.0.1:5000 in your browser and try the form.
