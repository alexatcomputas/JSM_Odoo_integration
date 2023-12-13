import logging

import functions_framework
from flask import Request

from customer import GetCustomer
from orders import GetOrders
from services.odoo import Odoo

# from models import Customer, Product, Sales_order

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

odoo = Odoo
# fields = odoo.env["stock.move.line"].fields_get()


@functions_framework.http
def main(request: Request):
    # request_json = request.get_json(silent=True)
    # request_args = request.args
    # issue_type = request.args["issue_type"]
    # ticket_email = request.args["email"]

    order_OK = False
    customer_OK = False

    try:
        serial_number = request.get_json()["serial_number"]
    except KeyError:
        logging.warning("Request failed (Serial number not found). Returning 404")
        return ("Request failed (Serial number not found)", 404)

    logging.info(f"Jira Service Management: Request received for SN:{serial_number}")
    logging.debug(f"Request json: {request.get_json(silent=False)}")

    # Get order data:
    try:
        Order = GetOrders(odoo=odoo, serial_number=serial_number)
        Order.get_order_data()
        order_OK = True

    except odoo.
    except Exception as e:
        logging.error(f"Error fetching order data:{e}")
        return (f"Failed obtaining order data on serial number {Order.serial_number}. Exiting", 500)

    # Get customer data:
    try:
        partner_id = Order.sale_order.partner_id[0]
        Customer = GetCustomer(odoo=odoo, partner_id=partner_id)
        Customer.fetch_customer_data()
        customer_OK = True

    except Exception as e:
        if Order.stockpicking.sale_id[1]:
            orderid = Order.stockpicking.sale_id[1]
            logging.error(
                f"Error fetching customer data from serial number {serial_number} and order id {orderid}:{e}"
            )
        else:
            logging.error(f"Error fetching customer data from serial number {serial_number}:{e}")

    if order_OK and customer_OK:
        logging.info("Success, returning order and customer data")
        return ("Success", 200)

    # TODO: Implement partial return
    elif order_OK:
        logging.info("Partial success, returning order data")
        return ("Partial success (Failed obtaining customer data)", 202)

    # TODO: Implement partial return
    # elif customer_OK:
    #     logging.info("Partial success, returning customer data")
    #     return ("Partial success (Failed obtaining order data)", 202)

    elif not order_OK and not customer_OK:
        return (f"Failed retrieving order and customer data on {serial_number}", 404)

    else:
        return ("Internal server error", 500)


if __name__ == "__main__":
    main()
