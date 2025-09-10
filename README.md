# ML Deployment Demo – Iris Classifier on Google Cloud Run

This repository demonstrates how to **train, save, and deploy a simple ML model** using [Google Cloud Run](https://cloud.google.com/run).
We use the classic **Iris dataset** to build a small classification model that predicts flower species based on sepal/petal measurements.

---

## Project Overview

* **Model:** Logistic Regression pipeline (scikit-learn) trained on the Iris dataset
* **Exported Artifact:** `model.joblib` (serialized model file)
* **Serving Framework:** Flask + Gunicorn
* **Deployment Target:** Google Cloud Run (serverless, auto-scaling, pay-per-use)

---

## Repository Structure

```
.
├── app.py              # Flask app serving the model
├── iris_training.ipynb # Training notebook for creating and exporting the model
├── model.joblib        # Trained scikit-learn model (exported)
├── requirements.txt    # Python dependencies
├── Dockerfile          # Container definition
└── README.md           # This file
```

---

## Local Setup (Optional)

If you want to run the app locally before deploying:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
gunicorn -b :8080 app:app
```

Then open: [http://localhost:8080](http://localhost:8080)

---

## Deploying to Google Cloud Run

1. Make sure you have [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed and initialized.

   ```bash
   gcloud auth login
   gcloud config set project YOUR_PROJECT_ID
   ```

2. cd into the directry containing the deployment files.

3. Deploy the service:

   ```bash
   gcloud run deploy iris-classifier \
     --source . \
     --region us-east1 \
     --allow-unauthenticated
   ```

4. Once deployed, you’ll get a **service URL** like:

   ```
   https://iris-classifier-xxxxxx-uc.a.run.app
   ```

---

## Example Request

Send a POST request with flower measurements (`sepal length`, `sepal width`, `petal length`, `petal width`):

```bash
URL="https://iris-classifier-xxxxxx-uc.a.run.app"
curl -s -X POST "$URL/predict" \
  -H "Content-Type: application/json" \
  -d '{"instances":[[5.1,3.5,1.4,0.2],[6.7,3.0,5.2,2.3]]}' | jq
```

**Sample Output:**

```json
{
  "predictions": [
    {
      "label": "setosa",
      "label_id": 0,
      "probs": [0.9808, 0.0191, 0.0000]
    },
    {
      "label": "virginica",
      "label_id": 2,
      "probs": [0.00005, 0.0434, 0.9564]
    }
  ]
}
```

---

## Troubleshooting

* Always check **Cloud Build logs** if a deployment fails:
  [Cloud Build Logs Console](https://console.cloud.google.com/cloud-build)
* If the service URL shows `SERVICE UNAVAILABLE`:

  * Confirm that the container **listens on port `8080`**.
  * Verify that `requirements.txt` contains compatible versions.
  * Check **Cloud Run logs** in [Logs Explorer](https://console.cloud.google.com/logs).

 You can also use the built-in **Gemini CLI in Cloud Shell** for troubleshooting, but always run it **inside the app directory** (not home `~`) so it has context.

---

## Next Steps

* Extend the app with more complex models.

---
