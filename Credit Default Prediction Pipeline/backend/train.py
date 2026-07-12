"""
train.py — Train the Credit Card Default Prediction model
and save it as model.pkl using joblib.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import RobustScaler
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, roc_auc_score
import joblib
import os

# ── 1. Load data ────────────────────────────────────────────────────────────
print("Loading dataset...")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
df = pd.read_csv(os.path.join(BASE_DIR, "UCI_Credit_Card.csv"))

# ── 2. Clean up column names ─────────────────────────────────────────────────
df.rename(columns={"default.payment.next.month": "default"}, inplace=True)
df.drop(columns=["ID"], inplace=True, errors="ignore")

# ── 3. Feature / target split ────────────────────────────────────────────────
FEATURES = [
    "LIMIT_BAL", "SEX", "EDUCATION", "MARRIAGE", "AGE",
    "PAY_0", "PAY_2", "PAY_3", "PAY_4", "PAY_5", "PAY_6",
    "BILL_AMT1", "BILL_AMT2", "BILL_AMT3", "BILL_AMT4", "BILL_AMT5", "BILL_AMT6",
    "PAY_AMT1", "PAY_AMT2", "PAY_AMT3", "PAY_AMT4", "PAY_AMT5", "PAY_AMT6",
]
TARGET = "default"

X = df[FEATURES]
y = df[TARGET]

# ── 4. Train / test split ────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(f"Train size: {len(X_train)}, Test size: {len(X_test)}")

# ── 5. Build preprocessing + model pipeline ──────────────────────────────────
numeric_features = FEATURES   # all features are numeric

preprocessor = ColumnTransformer(
    transformers=[
        ("num", Pipeline([
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler",  RobustScaler()),
        ]), numeric_features)
    ]
)

pipeline = Pipeline([
    ("preprocessor", preprocessor),
    ("classifier", LogisticRegression(
        max_iter=1000,
        random_state=42,
        class_weight="balanced",
    )),
])

# ── 6. Train ─────────────────────────────────────────────────────────────────
print("Training Logistic Regression pipeline...")
pipeline.fit(X_train, y_train)

# ── 7. Evaluate ───────────────────────────────────────────────────────────────
y_pred  = pipeline.predict(X_test)
y_proba = pipeline.predict_proba(X_test)[:, 1]

acc = accuracy_score(y_test, y_pred)
auc = roc_auc_score(y_test, y_proba)
print(f"\nAccuracy : {acc:.4f}")
print(f"ROC-AUC  : {auc:.4f}")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["No Default", "Default"]))

# ── 8. Save model ─────────────────────────────────────────────────────────────
model_path = os.path.join(BASE_DIR, "model.pkl")
joblib.dump({"pipeline": pipeline, "features": FEATURES}, model_path)
print(f"\nModel saved to: {model_path}")
