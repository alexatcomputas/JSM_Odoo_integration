from customer import GetCustomer
from models import Customer
from orders import Order
from response_models import ResponseModel


def strip_invalid_chars(string: str) -> str:
    # Replace , with . and : with ; and .. with .

    # Check if type is str else return it
    if not isinstance(string, str):
        return string

    else:
        return string.replace("..", ".")
        # return string.replace(",", ".").replace("..", ".")
        # return string.replace(",", ".").replace(":", ";").replace("..", ".")


# Build the response body based on the data we got from the Odoo db
def buildResponse(customer: GetCustomer = None, order: Order = None) -> ResponseModel:
    if not (customer or order):
        return ("Error building response. Missing customer or order data", 404)

    if not customer:
        customer = Customer(id=1, name="Unknown")

    def concatenate_product_names(products: list):
        """
        Concatenates the names of all products in the order.

        :param order: Order object with a list of Product objects.
        :return: A string with all product names concatenated.
        """
        # Using a list comprehension to extract names and 'join' to concatenate them
        return ", ".join(product.name for product in products)

    if order.so_line and isinstance(order.so_line, list):
        # I'm doing this in a rush please forgive me.
        # dash-concatenate each objects name attribute into one str (eg. "Name1 -  Name2 - Name3")
        name = " - ".join([obj.name for obj in order.so_line])
        quantity = order.so_line[0].quantity
        price_unit = order.so_line[0].price_unit

    data_fields = {
        "sale_order__name": strip_invalid_chars(order.sale_order.name) if order.sale_order.name else "",
        "sale_order__sent_BGL": strip_invalid_chars(order.sale_order.sent_BGL) if order.sale_order.sent_BGL else "",
        "sale_order__sent_Flex": strip_invalid_chars(order.sale_order.sent_Flex) if order.sale_order.sent_Flex else "",
        "sale_order__sent_Hapro": strip_invalid_chars(order.sale_order.sent_Hapro) if order.sale_order.sent_Hapro else "",
        "sale_order__customer_ref": strip_invalid_chars(order.sale_order.customer_ref) if order.sale_order.customer_ref else "",
        "sale_order__tracking_no": strip_invalid_chars(order.sale_order.tracking_no) if order.sale_order.tracking_no else "",
        # sale_order__tracking_no_flex: strip_invalid_chars(order.sale_order.tracking_no_flex)
        # if order.sale_order.tracking_no_flex else None # In case it's needed after all
        "res_partner__name": strip_invalid_chars(customer.name) if customer.name else "",
        "res_partner__street": strip_invalid_chars(customer.street) if customer.street else "",
        "res_partner__city": strip_invalid_chars(customer.city) if customer.city else "",
        "res_partner__postal_code": strip_invalid_chars(customer.postal_code) if customer.postal_code else "",
        "res_partner__state": strip_invalid_chars(customer.state[1]) if customer.state else "",
        "res_partner__country": strip_invalid_chars(customer.country[1]) if customer.country else "",
        "product_product__name": strip_invalid_chars(concatenate_product_names(order.products)) if order.products else "",
    }

    if order.so_line and isinstance(order.so_line, list):
        data_fields["sale_order_line__name"] = strip_invalid_chars(name) if name else ""
        data_fields["sale_order_line__quantity"] = strip_invalid_chars(quantity) if quantity else ""
        data_fields["sale_order_line__price_unit"] = strip_invalid_chars(price_unit) if price_unit else ""

    # The normal instance, not a list
    elif order.so_line:
        data_fields["sale_order_line__name"] = strip_invalid_chars(order.so_line.name) if order.so_line.name else ""
        data_fields["sale_order_line__quantity"] = order.so_line.quantity
        data_fields["sale_order_line__price_unit"] = order.so_line.price_unit

    else:
        data_fields["sale_order_line__name"] = ""
        data_fields["sale_order_line__quantity"] = 0
        data_fields["sale_order_line__price_unit"] = 0

    # Replace False with None for optional fields since they are returned as False from the Odoo db
    for key in data_fields:
        if data_fields[key] is False:
            data_fields[key] = ""

    return ResponseModel(
        sale_order__name=data_fields.get("sale_order__name"),
        sale_order__sent_BGL=data_fields.get("sale_order__sent_BGL"),
        sale_order__sent_Flex=data_fields.get("sale_order__sent_Flex"),
        sale_order__sent_Hapro=data_fields.get("sale_order__sent_Hapro"),
        sale_order__customer_ref=data_fields.get("sale_order__customer_ref"),
        sale_order_line__name=data_fields.get("sale_order_line__name"),
        sale_order_line__quantity=data_fields.get("sale_order_line__quantity"),
        sale_order_line__price_unit=data_fields.get("sale_order_line__price_unit"),
        sale_order__tracking_no=data_fields.get("sale_order__tracking_no"),
        # sale_order__tracking_no_flex=optional_fields.get("sale_order__tracking_no_flex"],
        res_partner__name=data_fields.get("res_partner__name"),
        res_partner__street=data_fields.get("res_partner__street"),
        res_partner__city=data_fields.get("res_partner__city"),
        res_partner__postal_code=data_fields.get("res_partner__postal_code"),
        res_partner__state=data_fields.get("res_partner__state"),
        res_partner__country=data_fields.get("res_partner__country"),
        product_product__name=data_fields.get("product_product__name"),
    )
