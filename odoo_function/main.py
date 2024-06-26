import json
import logging

import functions_framework
from flask import Request, jsonify
from werkzeug.exceptions import BadRequest

from customer import GetCustomer
from environment import ENVIRONMENT
from odoo import Odoo
from orders import Order
from response import buildResponse
from util import dump_request, process_and_jsonify_input

if ENVIRONMENT == "local":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.info("### Local environment detected ###")
else:
    logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
    logging.info("### Non-local environment detected ###")


@functions_framework.http
def main(request: Request):
    order_OK = False
    customer_OK = False

    serialnumber_fieldname = "serialnumber"

    try:
        serial_number = request.get_json(silent=False)["fields"][serialnumber_fieldname]

    except KeyError:
        logging.warning("Misconfigured request failed (Serial number field not found). 404")
        # return ("Request failed (Serial number field not found in request)", 404)
        serialized_data = process_and_jsonify_input("Request failed (Serial number field not found in request)")
        return serialized_data, 404

    except BadRequest as e:
        logging.error(f"Request failed (Bad request-> 400)\nRequest: {dump_request()}")
        logging.error(f"## Exception:##\n{e}")
        # return ("Invalid JSON", 400)
        serialized_data = process_and_jsonify_input("Invalid JSON")
        return serialized_data, 400

    except Exception as e:
        logging.error(f"Request failed -> 500:\nRequest: {dump_request()}")
        logging.error(f"## Exception:##\n{e}")
        # return ("Request failed (Unknown exception. Error logged). Returning 500", 500)
        serialized_data = process_and_jsonify_input("Request failed (Unknown exception. Error logged).")
        return serialized_data, 500

    logging.info(f"Jira Service Management: Request received for SN:{serial_number}")
    logging.debug(f"Request json: {request.get_json(silent=False)}")

    # Get order data #####
    try:
        order = Order(odoo=Odoo, serial_number=serial_number)
        order.get_order_data()
        if not order.stockmoveline == order.error_models.stockmoveline:
            order_OK = True

    except ValueError as ve:
        logging.error("Returning ValueError")
        # return (f"Failed obtaining order data on serial number {order.serial_number}. Error: {ve}", 404)
        serialized_data = process_and_jsonify_input(f"Failed obtaining order data on serial number {order.serial_number}. Error: {ve}")
        return serialized_data, 404

    except Exception as e:
        # Mandatory objects to populate for a meaningful order data response:
        # Order.picking_id -> Order.sale_id -> Order.product_id
        if order.picking_ids and not order.sale_id:
            logging.error(f"Error fetching order data on SN {order.serial_number} and picking id {order.picking_ids}")
        elif order.sale_id and not order.product_ids:
            logging.error(
                f"""Error fetching product data from picking model on SN:{order.serial_number},
                picking id {order.picking_id} and sale id {order.sale_id}"""
            )

        logging.error(f"### Stack trace: ###\n{e}")
        serialized_data = process_and_jsonify_input(f"Failed obtaining order data on serial number {order.serial_number}")
        return serialized_data, 404

    if not order.sale_order:
        logging.info("Serial number not found. Order data can't be built")
        serialized_data = process_and_jsonify_input(f"Serial number not found: {serial_number}")
        return serialized_data, 404

    # Get customer data #####
    try:
        customer = GetCustomer(odoo=Odoo, partner_id=order.sale_order.partner_id[0])
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
        # orderResponse = buildResponse(customer, order)
        serialized_data = process_and_jsonify_input(buildResponse(customer, order))

        return serialized_data, 200

    # Partial return
    elif order_OK:
        logging.info("Partial success, (Failed obtaining customer data). Only returning order data")
        logging.warning(f"Request: {dump_request()}")
        # responseData = serialize_response(buildResponse(customer=None, order=order))
        serialized_data = process_and_jsonify_input(buildResponse(customer=None, order=order))

        return serialized_data, 202

    elif not (order_OK and customer_OK):
        return (f"SN Error:Failed retrieving order and customer data on {serial_number}", 400)

    else:
        logging.error("Internal server error, 500")
        logging.error(f"Request: {dump_request()}")

        # responseData = serialize_response("Internal server error")
        serialized_data = process_and_jsonify_input("Internal server error")
        return serialized_data, 500


if __name__ == "__main__":
    main()
