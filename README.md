# Integration-JSM-Odoo
Main function of integration lies in the folder odoo_function

## Introduction
Integration for JSM and Odoo. Takes a JSM webrequest (POST) as input and fetches data from Odoo. Returns data to JSM automation to update ticket.
Created by Computas AS Oslo :smile:

## Special considerations
1. Prioritizes kit names when returning product info. To achieve this without hardcoding product names to prioritize, it simply gets all products associated with the serial number and selects the item that has "Kit" in the name. If no item with "Kit" is found, it will concatenate and return all the associated item names.
2. Only prod instance is running, stage can be deployed after fixing some SA permissions (access to secrets)
3. For changing passwords associated with the service, please access and add a secret version in Google Cloud Secrets Manager.
   - The secrets are named logically; odoo_prod_pass, odoo_prod_db and so on. access_password defines the password to interact with and get a token in return from the token_generator function