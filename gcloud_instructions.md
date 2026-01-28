
# Deploying Morning Bot to Google Cloud

Here are the instructions to deploy the Morning Bot script to Google Cloud Functions and schedule it to run daily using Cloud Scheduler.

For this, you need to have a Google Cloud account.

## Setup Instructions
1. Log in to your Google Cloud Console and create a new project (or select an existing one).

2. Enable the following APIs for your project:
   - Cloud Functions API
   - Cloud Build API
   - Cloud Scheduler API
   - IAM Service Account Credentials API

   You can do this via the Cloud Console or in Cloud Shell by running:
   ```bash
    gcloud services enable cloudfunctions.googleapis.com cloudscheduler.googleapis.com iamcredentials.googleapis.com cloudbuild.googleapis.com
    ```

3. Open Cloud Shell or set up `gcloud` CLI on your local machine.

4. Clone the repository and set up the virtual environment as above (steps 1-4).

5. Set up environment variables in `.env.yaml` file in the root directory.
   ```yaml
   WEATHER_API_KEY: "<your_weather_api_key>"
   YLE_API_ID: "<your_yle_api_id>"
   YLE_API_KEY: "<your_yle_api_key>"
   YLE_DOMESTIC_NEWS_PAGE: "102"
   YLE_INTERNATIONAL_NEWS_PAGE: "130"
   YLE_ECONOMY_NEWS_PAGE: "160"
   TELEGRAM_BOT_TOKEN: "<your_telegram_bot_token>"
   TELEGRAM_CHAT_ID: "<your_telegram_chat_id>"
   USER_LOCATION: "<your_city>" # e.g. "Helsinki", "New York", "Tokyo"
   USER_TIMEZONE: "<your_timezone>"  # e.g. "Europe/Helsinki", "America/New_York", "Asia/Tokyo"
   ```

6. Deploy to Google Cloud Functions (using Gen2 runtime)
   ```bash
   gcloud functions deploy morning-briefing \
   --runtime python311 \
   --region us-central1 \
   --source . \
   --entry-point morning_briefing \
   --trigger-http \
   --env-vars-file .env.yaml
   ```

7. Grant Cloud Scheduler permission to invoke the function

   Get project number:
   ```bash
   PROJECT_NUMBER=$(gcloud projects describe $(gcloud config get-value project) --format='value(projectNumber)')
   ```

   Allow the Compute Engine service account to invoke your function:
   ```bash
   gcloud functions add-invoker-policy-binding morning-briefing \
     --region=us-central1 \
     --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com"
   ```

8. Set up Cloud Scheduler to trigger the function daily at 7 AM

   Create the scheduler job:
   ```bash
   gcloud scheduler jobs create http morning-briefing-daily \
     --location=us-central1 \
     --schedule="0 7 * * *" \
     --time-zone="Europe/Helsinki" \
     --uri="https://us-central1-$(gcloud config get-value project).cloudfunctions.net/morning-briefing" \
     --http-method=POST \
     --oidc-service-account-email="$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
     --oidc-token-audience="https://us-central1-$(gcloud config get-value project).cloudfunctions.net/morning-briefing"
   ```
   
   **Change the timezone if needed** (e.g., `America/New_York`, `Asia/Tokyo`, `UTC`)

9. Test the setup by manually triggering the Cloud Scheduler job

   ```bash
   gcloud scheduler jobs run morning-briefing-daily --location=us-central1
   ```

   > NOTE: The run may take 2-3 minutes due to a "cold start" (Cloud Functions needs to spin up a container and load dependencies).


## Common Commands

**Run the function manually**      
```bash
gcloud functions call morning-briefing --region=us-central1
```

**Check scheduler status**      
```bash
gcloud scheduler jobs describe morning-briefing-daily --location=us-central1
```

**Pause (disable daily runs)**      
```bash
gcloud scheduler jobs pause morning-briefing-daily --location=us-central1
```

**Resume daily runs after pause**      
```bash
gcloud scheduler jobs resume morning-briefing-daily --location=us-central1
```

**Update the schedule (e.g., change to 8 AM)**    
```bash
gcloud scheduler jobs update http morning-briefing-daily \
  --location=us-central1 \
  --schedule="0 8 * * *"
```

**Recent function execution logs**      
```bash
gcloud functions logs read morning-briefing --region=us-central1 --limit=20
```

**Scheduler execution history** 
```bash
gcloud scheduler jobs describe morning-briefing-daily --location=us-central1
```

## Cost
You can monitor your Cloud Functions and Cloud Scheduler usage in the Google Cloud Console.     
Go to Billing → Reports      
Cloud Functions free tier is 2 million invocations/month so ~30 invocations/month (daily) should be well within it.
