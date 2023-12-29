import os

project_id = "690554692474"
ENVIRONMENT = os.getenv("environment", default="local")
AUTH_TOKEN = os.getenv("auth_token")


def get_secret_name(env=ENVIRONMENT, type="user"):
    return f"odoo_{env}_{type}"


if ENVIRONMENT != "local":
    ODOO_USERNAME = os.getenv(get_secret_name(type="user"))  # odoo_prod_user
    ODOO_PASSWORD = os.getenv(get_secret_name(type="pass"))  # odoo_prod_pass
    ODOO_SERVER = os.getenv(get_secret_name(type="server"))  # odoo_prod_server
    ODOO_DATABASE = os.getenv(get_secret_name(type="db"))  # odoo_prod_db

else:
    ODOO_USERNAME = os.getenv("odoo_user")
    ODOO_PASSWORD = os.getenv("odoo_pass")
    ODOO_SERVER = os.getenv("odoo_server")
    ODOO_DATABASE = os.getenv("odoo_db")
