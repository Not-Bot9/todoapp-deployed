

# To-Do App - Google Cloud Run Deployment Demo

This is a very simple Flask to-do application designed to demonstrate how to **containerize** and **deploy** an app to **Google Cloud Run**.
It doesn’t use any databases - all notes exist only in memory during runtime.

The main purpose of this repo is for the AI/ML team to **learn Cloud Run deployment workflow** before deploying larger ML models.

---

## Prerequisites

1. A **Google Cloud account** with billing enabled.
2. **Google Cloud SDK** (gcloud) installed, OR use **Cloud Shell** from the GCP Console (recommended).
3. Enable the **Cloud Run API** and **Cloud Build API** in your project (if not already enabled):

   ```bash
   gcloud services enable run.googleapis.com cloudbuild.googleapis.com
   ```

---

## Deploying to Cloud Run

From Cloud Shell or your terminal:

1. **Clone this repo** (or open it in Cloud Shell):

   ```bash
   git clone https://github.com/<your-org>/<repo-name>.git
   cd <repo-name>/test_app
   ```

2. **Deploy the app to Cloud Run** (from inside the project folder):

   ```bash
   gcloud run deploy todoapp --source . --region us-east1 --allow-unauthenticated
   ```

   * `--source .` tells Cloud Build to build from the current directory.
   * `--region us-east1` chooses a deployment region (change if needed).
   * `--allow-unauthenticated` lets anyone access the app.

3. Wait for the build → deploy → traffic routing steps to complete.
   At the end you’ll get a **Service URL** like:

   ```
   https://todoapp-xxxxxx-uc.a.run.app
   ```

4. Open the URL in your browser to see the app live.

---

## Redeploying (with new changes)

If you update the code and want to redeploy:

```bash
gcloud run deploy todoapp --source . --region us-east1
```

You can also deploy under a new name (e.g., `todoapp-2`) to test side-by-side versions.

---

## Troubleshooting

* Always make sure you’re in the **directory that contains your app files** before running `gcloud run deploy`.
* If you hit errors during build/deploy, try the **Gemini CLI tool** available in Cloud Shell.

  * Open a **new Cloud Shell tab**
  * Navigate (`cd`) into the project directory (not home `~`)
  * Run:

    ```bash
    gemini help
    ```

  Gemini will use your local context (the app files) to debug.

---

## Notes

* We’re using **Dockerfile build** by default. If you don’t include a Dockerfile, Cloud Run will try Buildpacks.
* Default machine spec is 1 CPU, 512MB RAM. For heavier workloads you can increase it with:

  ```bash
  gcloud run deploy todoapp --source . --region us-east1 --cpu=1 --memory=2Gi
  ```
* The app is ephemeral (no DB). Restarting will reset your notes.

---

## Next Steps

* Try editing the app (add new routes, change UI) and redeploy.
* Experiment with scaling options (`--max-instances`, `--min-instances`) (might increase costs).
* After this, we’ll practice deploying a **small pre-trained ML model** before moving to full production models.

---


