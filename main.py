import logging

import functions_framework
from flask import Request

from customer import GetCustomer
from orders2 import GetOrders
from services.odoo import Odoo

# from models import Customer, Product, Sales_order

logging.basicConfig(level=logging.info, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

odoo = Odoo


@functions_framework.http
def main(request: Request):
    # request_json = request.get_json(silent=True)
    # request_args = request.args

    # issue_type = request.args["issue_type"]
    # ticket_email = request.args["email"]
    try:
        serial_number = request.get_json()["serial_number"]
    except KeyError:
        logging.warning(f"Bad request, SN not found. Returning 400")
        return ("Bad request. Serial number not found", 400)

    logging.info(f"Request received. SN:{serial_number}")
    print(request.get_json(silent=True))

    logging.debug("Proceeding")
    logging.debug(f"Request json: {request.get_json(silent=True)}")

    Order = GetOrders(odoo=odoo, serial_number=serial_number)
    Order.get_order_data()
    Order.extract_order_data()

    # Get customer data:
    customer_id = Order.sale_order.partner_id[0]
    # ticket_email = request.get_json()["email"]
    # ticket_email = "email@email.com"
    Customer = GetCustomer()
    customer_data = Customer.fetch_customer_data(odoo=odoo, partner_id=customer_id)

    return ("Success", 200)


if __name__ == "__main__":
    main()
