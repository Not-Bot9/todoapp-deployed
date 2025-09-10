import os
import json
import joblib
import numpy as np
from flask import Flask, request, jsonify

# Load model once at startup    
BUNDLE = joblib.load(os.environ.get("MODEL_PATH", "model.joblib"))
MODEL = BUNDLE["model"]
FEATURES = BUNDLE["feature_names"]  # ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
TARGET_NAMES = BUNDLE["target_names"]  # ['setosa','versicolor','virginica']

app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/predict")
def predict():
    """
    Accepts JSON:
      {"instances":[ [5.1,3.5,1.4,0.2], [6.7,3.0,5.2,2.3] ]}
    or:
      {"instances":[ {"sepal length (cm)":5.1,"sepal width (cm)":3.5,"petal length (cm)":1.4,"petal width (cm)":0.2} ]}
    Returns predictions with probabilities.
    """
    payload = request.get_json(silent=True) or {}
    instances = payload.get("instances", [])

    if not instances:
        return jsonify(error="Provide 'instances' as list of rows."), 400

    # Normalize inputs to array
    rows = []
    for row in instances:
        if isinstance(row, dict):
            rows.append([row.get(f) for f in FEATURES])
        else:
            rows.append(row)
    X = np.array(rows, dtype=float)

    if X.ndim != 2 or X.shape[1] != len(FEATURES):
        return jsonify(error=f"Each row must have {len(FEATURES)} features in order {FEATURES}"), 400

    probs = MODEL.predict_proba(X).tolist()
    labels = MODEL.predict(X).tolist()
    label_names = [TARGET_NAMES[i] for i in labels]

    return jsonify(
        predictions=[
            {"label_id": int(li), "label": ln, "probs": p}
            for li, ln, p in zip(labels, label_names, probs)
        ]
    )

@app.get("/")
def root():
    return jsonify(
        message="Iris classifier is running.",
        features=FEATURES,
        target_names=TARGET_NAMES,
        usage="POST /predict with JSON {'instances': [[...],[...]]}"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
