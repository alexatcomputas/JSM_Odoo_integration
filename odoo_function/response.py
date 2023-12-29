from customer import GetCustomer
from orders import Order
from response_models import returnModel


def strip_invalid_chars(string: str) -> str:
    # Replace , with .
    # Replace : with ;
    return string.replace(",", ".").replace(":", ";").replace("..", ".")


# Build the response body based on the data we got from the Odoo db
def buildResponse(customer: GetCustomer = None, order: Order = None) -> returnModel:
    if not (customer and order):
        return ("Error building response. Missing customer and order data", 401)

    data_fields = {
        "sale_order__name": strip_invalid_chars(order.sale_order.name) if order.sale_order.name else None,
        "sale_order__sent_BGL": strip_invalid_chars(order.sale_order.sent_BGL) if order.sale_order.sent_BGL else None,
        "sale_order__sent_Flex": strip_invalid_chars(order.sale_order.sent_Flex) if order.sale_order.sent_Flex else None,
        "sale_order__sent_Hapro": strip_invalid_chars(order.sale_order.sent_Hapro) if order.sale_order.sent_Hapro else None,
        "sale_order__customer_ref": strip_invalid_chars(order.sale_order.customer_ref) if order.sale_order.customer_ref else None,
        "sale_order_line__name": strip_invalid_chars(order.so_line.name) if order.so_line.name else None,
        "sale_order_line__quantity": order.so_line.quantity,
        "sale_order_line__price_unit": order.so_line.price_unit,
        "sale_order__tracking_no": strip_invalid_chars(order.sale_order.tracking_no) if order.sale_order.tracking_no else None,
        # sale_order__tracking_no_flex: strip_invalid_chars(order.sale_order.tracking_no_flex)
        # if order.sale_order.tracking_no_flex else None # In case it's needed after all
        "res_partner__name": strip_invalid_chars(customer.name) if customer.name else None,
        "res_partner__street": strip_invalid_chars(customer.street) if customer.street else None,
        "res_partner__city": strip_invalid_chars(customer.city) if customer.city else None,
        "res_partner__postal_code": strip_invalid_chars(customer.postal_code) if customer.postal_code else None,
        "res_partner__state": strip_invalid_chars(customer.state[1]) if customer.state else None,
        "res_partner__country": strip_invalid_chars(customer.country[1]) if customer.country else None,
    }

    # Replace False with None for optional fields since they are returned as False from the Odoo db
    for key in data_fields:
        if data_fields[key] is False:
            data_fields[key] = None

    return returnModel(
        sale_order__name=data_fields["sale_order__name"],
        sale_order__sent_BGL=data_fields["sale_order__sent_BGL"],
        sale_order__sent_Flex=data_fields["sale_order__sent_Flex"],
        sale_order__sent_Hapro=data_fields["sale_order__sent_Hapro"],
        sale_order__customer_ref=data_fields["sale_order__customer_ref"],
        sale_order_line__name=data_fields["sale_order_line__name"],
        sale_order_line__quantity=data_fields["sale_order_line__quantity"],
        sale_order_line__price_unit=data_fields["sale_order_line__price_unit"],
        sale_order__tracking_no=data_fields["sale_order__tracking_no"],
        # sale_order__tracking_no_flex=optional_fields["sale_order__tracking_no_flex"],
        res_partner__name=data_fields["res_partner__name"],
        res_partner__street=data_fields["res_partner__street"],
        res_partner__city=data_fields["res_partner__city"],
        res_partner__postal_code=data_fields["res_partner__postal_code"],
        res_partner__state=data_fields["res_partner__state"],
        res_partner__country=data_fields["res_partner__country"],
    )
