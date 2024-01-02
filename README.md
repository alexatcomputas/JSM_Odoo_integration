# Integration-JSM-Odoo
Main function of integration lies in the folder odoo_function

## Introduction
Integration for JSM and Odoo. Takes a JSM webrequest (POST) as input and fetches data from Odoo. Returns data to JSM automation to update ticket.
Created by Computas AS Oslo :smile:

## Special considerations
- The integration function has no capability programmed in to write to the database, it can only access odoo to read its content.
- Data on the serial number is read in and processed and returned in response to the webrequest from Jira's automation
   1. Serial number POST'ed to function
   2. Function performs several searches in Odoo on the models:
      1. stock.move.line
      2. production.lot
      3. stock.picking
      4. sale.order
      5. Sale.Order.Line
   3. Retrieved data is compiled and returned in resposne to Jira Service Management's automation
   4. JSM automation interprets resposne and saves data into ticket
- Prioritizes kit names when returning product info. To achieve this without hardcoding product names to prioritize, it simply gets all products associated with the serial number and selects the item that has "Kit" in the name. If no item with "Kit" is found, it will concatenate and return all the associated item names.
- Only prod instance is running, stage can be deployed after fixing some SA permissions (access to secrets)
- For changing passwords associated with the service, please access and add a secret version in Google Cloud Secrets Manager.
   - The secrets are named logically; odoo_prod_pass, odoo_prod_db and so on. access_password defines the password to interact with and get a token in return from the token_generator function