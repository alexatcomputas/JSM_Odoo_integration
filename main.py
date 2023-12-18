import logging

import functions_framework
from flask import Request

from customer import GetCustomer
from orders import Order
from response import buildResponse
from services.odoo import Odoo

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
        order = Order(odoo=odoo, serial_number=serial_number)
        order.get_order_data()
        order_OK = True

    except Exception as e:
        # Order.picking_id -> Order.sale_id -> Order.product_id
        if order.picking_id and not order.sale_id:
            logging.error(f"Error fetching order data on SN {order.serial_number} and picking id {order.picking_id}")
        elif order.sale_id and not order.product_id:
            logging.error(
                f"Error fetching product data on picking SN {order.serial_number}, picking id {order.picking_id} and sale id {order.sale_id}"
            )

        logging.error(f"### Stack trace: ###\n{e}")
        return (f"Failed obtaining order data on serial number {order.serial_number}. Exiting", 500)

    # Get customer data:
    try:
        partner_id = order.sale_order.partner_id[0]
        customer = GetCustomer(odoo=odoo, partner_id=partner_id)
        customer_OK = True

    except Exception as e:
        if order and hasattr(order, "stockpicking") and order.stockpicking:
            if hasattr(order.stockpicking, "sale_id") and order.stockpicking.sale_id:
                orderid = order.stockpicking.sale_id[1]
                logging.error(
                    f"Error fetching customer data from serial number {serial_number} and order id {orderid}:{e}"
                )
        else:
            logging.error(f"Error fetching customer data from serial number {serial_number}:{e}")

    if order_OK and customer_OK:
        logging.info(f"Success, returning order [{order.sale_order.name}] and customer data to JSM")

        orderResponse = buildResponse(order, customer)
        print(orderResponse.model_dump_json(by_alias=True, exclude_none=True))

        # customerResponse = buildCustomerResponse(customer)
        # print(customerResponse.model_dump_json(by_alias=True, exclude_none=True))

        return ("Success", 200)

    # TODO: Implement partial return
    elif order_OK:
        logging.info("Partial success, (Failed obtaining customer data). Only returning order data")
        return ("Partial success, (Failed obtaining customer data). Only returning order data", 202)

    elif not (order_OK and customer_OK):
        return (f"Failed retrieving order and customer data on {serial_number}", 404)

    else:
        return ("Internal server error", 500)


if __name__ == "__main__":
    main()
