import logging

from odoorpc import ODOO

from models import Customer

logging.basicConfig()
# logger = logging.getLogger("odoorpc")
logger = logging.getLogger("local")
logger.setLevel(logging.DEBUG)


class GetCustomer:
    def fetch_customer_data(self, odoo: ODOO, partner_id: int) -> Customer:
        partner_obj = odoo.env["res.partner"]
        id = partner_id

        # Fetch customer data based on id
        partner_id = partner_obj.search([("id", "=", id)], limit=1)[0]
        if not partner_id:
            # Partner not found
            logging.error(f"Partner [{id}] not found in partner db.")
            return Customer(id=-1, email="none@notfound.com")

        # Partner found, process the partner data
        logging.info(f"Proceeding to fetch customer data on {partner_id}.")
        fields_to_fetch = ["name", "email", "street", "city", "zip", "state_id", "country_id", "ref", "is_company"]
        partner_details = partner_obj.read(partner_id, fields_to_fetch)[0]

        customer_data = {
            "id": partner_id,
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
        logging.debug(f"Returning customer data on customer [{partner_id}], {len(customer_data)} items")

        return Customer(**customer_data)
