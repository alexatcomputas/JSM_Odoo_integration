import logging

from odoorpc import ODOO

from models import Customer


class GetCustomer:
    def __init__(self, odoo: ODOO, partner_id: str):
        self.odoo = odoo
        self.partner_id = partner_id
        self.resPartner = odoo.env["res.partner"]
        self.customer_data = None

    def fetch_customer_data(self) -> Customer:
        id = self.partner_id
        partner_object = self.resPartner

        logging.info(f"Fetching customer data on ID:{id}.")
        fields_to_fetch = ["name", "email", "street", "city", "zip", "state_id", "country_id", "ref", "is_company"]
        partner_details = partner_object.read(id, fields_to_fetch)[0]

        customer_data = {
            "id": id,
            "email": partner_details.get("email", None),
            "name": partner_details.get("name", None),
            "street": partner_details.get("street", None),
            "city": partner_details.get("city", None),
            "postal_code": partner_details.get("zip", None),
            "state": partner_details.get("state_id", None),
            "country": partner_details.get("country_id", None),
            "customer_reference": partner_details.get("ref", None),
            "is_company": partner_details.get("is_company", None),
        }

        logging.debug(f"Returning data on customer [{id}: {customer_data.name}]")
        self.customer_data = Customer(**customer_data)
