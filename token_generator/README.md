# Token generator

- Cloud function (allow-unauthenticated)
- Requires password for code execution

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
