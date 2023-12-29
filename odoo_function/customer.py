import logging

from odoorpc import ODOO


class GetCustomer:
    def __init__(self, odoo: ODOO, partner_id: str):
        self.odoo = odoo
        self.partner_id = partner_id
        self.resPartner = odoo.env["res.partner"]
        self.email = None
        self.name = None
        self.street = None
        self.city = None
        self.postal_code = None
        self.state = None
        self.country = None
        self.customer_reference = None
        self.is_company = None
        self.customer_data = None

        # Fetch customer data and populate fields
        self.fetch_customer_data()

    def fetch_customer_data(self):
        id = self.partner_id
        partner_object = self.resPartner

        logging.info(f"Fetching customer data on ID:{id}.")
        fields_to_fetch = ["name", "email", "street", "city", "zip", "state_id", "country_id", "ref", "is_company"]
        partner_details = partner_object.read(id, fields_to_fetch)[0]

        logging.debug(f"Returning data on customer [{id}: {partner_details.get('name', None)}]")

        self.email = partner_details.get("email", None)
        self.name = partner_details.get("name", None)
        self.street = partner_details.get("street", None)
        self.city = partner_details.get("city", None)
        self.postal_code = partner_details.get("zip", None)
        self.state = partner_details.get("state_id", None)
        self.country = partner_details.get("country_id", None)
        self.customer_reference = partner_details.get("ref", None)
        self.is_company = partner_details.get("is_company", None)
