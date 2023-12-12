import os

import odoorpc
from dotenv import load_dotenv

load_dotenv()

# Odoo Configuration.
# TODO: Get data from secrets
ODOO_SERVER = os.getenv("odoo_server")
ODOO_DATABASE = os.getenv("odoo_db")
ODOO_USERNAME = os.getenv("odoo_username")
ODOO_PASSWORD = os.getenv("odoo_pass")

# Initialize Odoo RPC
Odoo = odoorpc.ODOO(ODOO_SERVER, protocol="jsonrpc+ssl", port=443)
Odoo.login(ODOO_DATABASE, ODOO_USERNAME, ODOO_PASSWORD)
