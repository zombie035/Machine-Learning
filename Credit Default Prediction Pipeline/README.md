# 💳 Credit Card Default Prediction — Deployable Web App

An end-to-end machine learning project that predicts whether a credit card customer will **default on their next payment**. Converted from a Jupyter notebook into a fully deployable **Flask API + rich web UI**.

---

## 📁 Project Structure

```
Credit Default Prediction Pipeline/
├── backend/
│   ├── app.py               # Flask REST API (serves frontend + /predict endpoint)
│   ├── train.py             # Model training script → produces model.pkl
│   ├── requirements.txt     # Python dependencies
│   └── UCI_Credit_Card.csv  # Dataset (30,000 samples, UCI repository)
├── frontend/
│   ├── index.html           # Main UI (premium white theme)
│   ├── style.css            # Styles
│   └── app.js               # Frontend logic (fetch, form validation, gauge)
├── credit_default_project.ipynb  # Original exploratory notebook
└── README.md
```

---

## 🚀 Quick Start

### 1. Install dependencies
```bash
cd backend
pip install -r requirements.txt
```

### 2. Train the model
```bash
python train.py
```
This trains a **Logistic Regression** pipeline (with RobustScaler) on the UCI dataset and saves `model.pkl`.

**Evaluation on held-out test set (6,000 samples):**
| Metric | Score |
|---|---|
| Accuracy | 67.9% |
| ROC-AUC  | 70.8% |

### 3. Start the Flask server
```bash
python app.py
```

### 4. Open the Web UI
Visit **http://localhost:5000** in your browser.

---

## 🖥️ Web UI Features

- **4-section input form** — Personal Info, Repayment Status, Bill Amounts, Payment Amounts
- **Quick-fill buttons** — Load Low Risk or High Risk sample data instantly
- **Animated probability gauge** — Visual circular meter showing default probability
- **Risk breakdown panel** — Prediction label, probability %, and risk level (Low / Medium / High)
- **Form validation** — Highlights missing fields before submission
- **Premium white theme** — Clean, modern design with Inter font and subtle shadows

---

## 🧠 ML Pipeline

| Step | Detail |
|---|---|
| Dataset | UCI Credit Card Clients (Taiwan, 2005) |
| Samples | 30,000 (train: 24,000 / test: 6,000) |
| Features | 23 (demographics, payment history, bill & payment amounts) |
| Preprocessing | `SimpleImputer` + `RobustScaler` via `ColumnTransformer` |
| Model | `LogisticRegression(max_iter=1000, class_weight='balanced')` |
| Serialization | `joblib` (model.pkl) |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Serves the frontend UI |
| GET | `/health` | Model status + feature list |
| POST | `/predict` | Returns prediction + probability |

**POST /predict** — example request body:
```json
{
  "LIMIT_BAL": 200000, "SEX": 1, "EDUCATION": 1, "MARRIAGE": 2, "AGE": 30,
  "PAY_0": -1, "PAY_2": -1, "PAY_3": -1, "PAY_4": -1, "PAY_5": -1, "PAY_6": -1,
  "BILL_AMT1": 15000, "BILL_AMT2": 14000, "BILL_AMT3": 12000,
  "BILL_AMT4": 10000, "BILL_AMT5": 9000,  "BILL_AMT6": 8000,
  "PAY_AMT1": 15000,  "PAY_AMT2": 14000,  "PAY_AMT3": 12000,
  "PAY_AMT4": 10000,  "PAY_AMT5": 9000,   "PAY_AMT6": 8000
}
```

**Response:**
```json
{
  "prediction": 0,
  "probability": 0.2696,
  "probability_pct": 27.0,
  "risk_level": "Low",
  "label": "Will NOT Default"
}
```

---

## 📊 Dataset

- **Source:** [UCI Machine Learning Repository](https://archive.ics.uci.edu/dataset/350/default+of+credit+card+clients)
- **Target variable:** `default.payment.next.month` (1 = default, 0 = no default)
- **Class imbalance:** ~22% default rate → handled with `class_weight='balanced'`
