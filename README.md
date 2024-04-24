# Integration-JSM-Odoo
Main function of integration lies in the folder odoo_function

## Introduction
Integration for JSM and Odoo. Takes a JSM webrequest (POST) as input and fetches data from Odoo. Returns data to JSM automation to update ticket.
Created by Computas AS Oslo :smile:

## Special considerations
- The integration function has no capability programmed in to write to the database, it can only access odoo to read its content.
- Data on the serial number is read in and processed and returned in response to the webrequest from Jira's automation
   1. Webrequest number 1:
      - Performs a request to a google cloud function with a strong password and an environment variable (prod/stage). The response (if password is valid) is a token to access the odoo_prod/stage function
   2. Webrequest number 2:
      - Function url: POST [odoo_prod GCP cloud function](https://europe-west1-integration-jsm-odoo.cloudfunctions.net/odoo_prod)
      - Serial number POST'ed to function with accompanying token attained from previous cloud function. Function performs several searches in Odoo on the models:
        - stock.move.line, production.lot, stock.picking, sale.order, Sale.Order.Line, res.partner
      - Retrieved data is compiled and returned in response to Jira Service Management's automation
   3. JSM automation interprets response and saves data into ticket
- Prioritizes kit names when returning product info. To achieve this without hardcoding product names to prioritize, it simply gets all products associated with the serial number and selects the item that has "Kit" in the name. If no item with "Kit" is found, it will concatenate and return all the associated item names.
- Only prod instance is running, stage can be deployed after fixing some SA permissions (Minor. Requires access to secrets)
- For changing passwords associated with the service, please access and add a secret version in Google Cloud Secrets Manager.
   - The secrets are named logically:
     - odoo_prod_user
     - odoo_prod_pass
     - odoo_prod_server
     - odoo_prod_db
     - access_password defines the password to interact with and get a token in return from the token_generator function
   - When adding new passwords and such, please do only add new versions of the secret. The function will be able to access only the newest version of the secret.
 - **SECURITY CONSIDERATION** Please add a very strong password asaccess_password, and keep minimum viable access in mind, limit all access to the given token/service account to strictly allow invoking the next cloud function. No other privileges should be granted.