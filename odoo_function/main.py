import logging
import re

import functions_framework
import google.cloud.logging
from flask import Request
from werkzeug.exceptions import BadRequest

from customer import GetCustomer
from environment import AUTH_TOKEN, ENVIRONMENT
from odoo import Odoo
from orders import Order
from response import buildResponse

if ENVIRONMENT == "local":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
else:
    logging_client = google.cloud.logging.Client()
    logging_client.setup_logging()

odoo = Odoo


@functions_framework.http
def main(request: Request):
    token_valid = False
    incoming_token = None

    # Extract the token from the request headers
    incoming_token = request.headers.get("Authorization")

    # Validate the token format (example: Bearer [token])
    if incoming_token and re.match(r"^Bearer [A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+$", incoming_token):
        token = incoming_token.replace("Bearer ", "")  # Extract the token part
        if token == AUTH_TOKEN:
            token_valid = True

    if not token_valid:
        return ("Invalid token or invalid token format", 401)

    order_OK = False
    customer_OK = False
    serial_number_customfieldid = "customfield_10408"

    try:
        serial_number = request.get_json(silent=False)["fields"][serial_number_customfieldid]
    except KeyError:
        logging.warning("Request failed (Serial number not found). Returning 404")
        return ("Request failed (Serial number not found in request)", 404)
    except BadRequest as e:
        logging.error(f"Request failed (Bad request. Error logged). Returning 400\n### Stack trace: ###\n{e}")
        return ("Invalid JSON", 400)
    except Exception as e:
        logging.error(f"Request failed (Any other Exception)\n### Stack trace: ###\n{e}")
        return ("Request failed (Unknown exception. Error logged). Returning 500", 500)

    logging.info(f"Jira Service Management: Request received for SN:{serial_number}")
    logging.debug(f"Request json: {request.get_json(silent=False)}")

    # Get order data #####
    try:
        order = Order(odoo=odoo, serial_number=serial_number)
        order.get_order_data()
        order_OK = True
    except Exception as e:
        # Mandatory objects to populate for a meaningful order data response:
        # Order.picking_id -> Order.sale_id -> Order.product_id
        if order.picking_ids and not order.sale_id:
            logging.error(f"Error fetching order data on SN {order.serial_number} and picking id {order.picking_id}")
        elif order.sale_id and not order.product_ids:
            logging.error(
                f"""Error fetching product data from picking model on SN:{order.serial_number},
                picking id {order.picking_id} and sale id {order.sale_id}"""
            )

        logging.error(f"### Stack trace: ###\n{e}")
        return (f"Failed obtaining order data on serial number {order.serial_number}. Exiting", 500)

    # Get customer data #####
    try:
        customer = GetCustomer(odoo=odoo, partner_id=order.sale_order.partner_id[0])
        customer_OK = True

    except Exception as e:
        if order and hasattr(order, "stockpicking") and order.stockpicking:
            if hasattr(order.stockpicking, "sale_id") and order.stockpicking.sale_id:
                orderid = order.stockpicking.sale_id[1]
                logging.error(
                    f"Error fetching customer data from serial number {serial_number} and order id {orderid}:\n### Stack trace: ###\n{e}"
                )
        else:
            logging.error(f"Error fetching customer data from serial number {serial_number}:\n### Stack trace: ###\n{e}")

    if order_OK and customer_OK:
        logging.info(f"Success, returning order [{order.sale_order.name}] and customer data to JSM")
        # orderResponseClass = buildResponse(customer, order)
        orderResponse = buildResponse(customer, order).model_dump_json(by_alias=True, exclude_none=False)

        return (orderResponse, 200)

    # Partial return
    elif order_OK:
        logging.info("Partial success, (Failed obtaining customer data). Only returning order data")
        # orderResponseClass = buildResponse(customer=customer)
        orderResponse = buildResponse(customer=customer).model_dump_json(by_alias=True, exclude_none=False)

        return (orderResponse, 202)

    elif not (order_OK and customer_OK):
        return (f"SN Error:Failed retrieving order and customer data on {serial_number}", 404)

    else:
        return ("Internal server error", 500)


if __name__ == "__main__":
    main()
