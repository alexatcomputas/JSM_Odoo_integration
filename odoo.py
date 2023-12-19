import odoorpc

from environment import ODOO_DATABASE, ODOO_PASSWORD, ODOO_SERVER, ODOO_USERNAME

# Odoo Configuration
# Initialize Odoo RPC
Odoo = odoorpc.ODOO(ODOO_SERVER, protocol="jsonrpc+ssl", port=443)
Odoo.login(ODOO_DATABASE, ODOO_USERNAME, ODOO_PASSWORD)
