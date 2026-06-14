from pathlib import Path

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import train_test_split


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "training_companies.csv"
MODEL_PATH = BASE_DIR / "credit_model.pkl"

FEATURES = [
    "z_score",
    "working_capital_to_assets",
    "retained_earnings_to_assets",
    "ebit_to_assets",
    "market_value_to_liabilities",
    "sales_to_assets",
    "debt_to_assets",
    "debt_to_market_value",
]

_model = None
_metrics = None


def train_model():
    df = pd.read_csv(DATA_PATH)
    x = df[FEATURES]
    y = df["bankrupt"]

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=42, stratify=y
    )

    model = RandomForestClassifier(
        n_estimators=160,
        max_depth=6,
        min_samples_leaf=3,
        random_state=42,
        class_weight="balanced",
    )
    model.fit(x_train, y_train)

    predictions = model.predict(x_test)
    probabilities = model.predict_proba(x_test)[:, 1]

    metrics = {
        "accuracy": round(accuracy_score(y_test, predictions), 3),
        "precision": round(precision_score(y_test, predictions), 3),
        "recall": round(recall_score(y_test, predictions), 3),
        "f1_score": round(f1_score(y_test, predictions), 3),
        "roc_auc": round(roc_auc_score(y_test, probabilities), 3),
        "model": "RandomForestClassifier",
        "features": FEATURES,
    }

    joblib.dump({"model": model, "metrics": metrics}, MODEL_PATH)
    return model, metrics


def load_model():
    global _model, _metrics
    if _model is not None:
        return _model, _metrics
    if MODEL_PATH.exists():
        payload = joblib.load(MODEL_PATH)
        _model = payload["model"]
        _metrics = payload["metrics"]
    else:
        _model, _metrics = train_model()
    return _model, _metrics


def predict_risk(features):
    model, _ = load_model()
    row = pd.DataFrame([{name: features[name] for name in FEATURES}])
    return round(float(model.predict_proba(row)[0][1]) * 100, 2)


def model_metrics():
    _, metrics = load_model()
    return metrics
