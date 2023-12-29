# Token generator

- Cloud function (allow-unauthenticated)
- Requires password for code execution
- Runs on minimum available cloud functions spec, 0-2 instances

## Introduction
This function was implemented as a workaround because JSM automation is missing a good function for storing access credentials to access oauth2.0 applications securely.
Takes a large password and returns severely restricted ID-token that has limited authorization of invoking odoo_prod\/odoo_stage depending on header specification

## REST
- Function url: POST [GCP cloud function URL](https://europe-west1-integration-jsm-odoo.cloudfunctions.net/token_generator)
- Required headers:
  - password: strong password
  - environment: [stage | prod]
- Returns:
  - ID token from JWT grant (1h duration, non-changeable as per GCP standards)

## Deploy
### GCP CLI
>gcloud functions deploy token_generator \
 --gen2 \
 --region=europe-west1 \
 --source=. \
 --min-instances 0 \
 --max-instances 2 \
 --timeout 120 \
 --set-env-vars='stage_audience'='https://europe-west1-integration-jsm-odoo.cloudfunctions.net/odoo_stage','prod_audience'='https://www.google.com' \
  --entry-point main \
  --runtime python311 \
  --trigger-http \
  --allow-unauthenticated \
  --set-secrets='PROD_CREDENTIALS'=PROD_CREDENTIALS:latest,'STAGE_CREDENTIALS'=STAGE_CREDENTIALS:latest,access_password='access_password:latest' \
  --service-account jsm-trigger-account@integration-jsm-odoo.iam.gserviceaccount.com \
  --project integration-jsm-odoo

TODO: Set up Terraform instead for deployment tasks (No time for now)