import os

ENVIRONMENT = os.getenv("environment", default="cloud")
ODOO_USERNAME = os.getenv("odoo_user")
ODOO_PASSWORD = os.getenv("odoo_pass")
ODOO_SERVER = os.getenv("odoo_server")
ODOO_DATABASE = os.getenv("odoo_db")
