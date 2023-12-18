from customer import GetCustomer
from orders import Order
from response_models import returnModel


def buildResponse(order: Order, customer: GetCustomer) -> returnModel:
    sale_order__name = order.sale_order.name

    optional_fields = {
        "sale_order__sent_BGL": order.sale_order.sent_BGL,
        "sale_order__sent_Flex": order.sale_order.sent_Flex,
        "sale_order__sent_Hapro": order.sale_order.sent_Hapro,
        "sale_order__customer_ref": order.sale_order.customer_ref,
        "sale_order_line__name": order.so_line.name,
        "sale_order_line__quantity": order.so_line.quantity,
        "sale_order_line__price_unit": order.so_line.price_unit,
        "sale_order__tracking_no": order.sale_order.tracking_no
        # sale_order__tracking_no_flex: order.sale_order.tracking_no_flex # In case it's needed after all
    }

    # Replace False with None for optional fields since they are set as False in the Odoo db
    for key in optional_fields:
        if optional_fields[key] is False:
            optional_fields[key] = None

    custAddress = customer.jsm_return_custAddress

    return returnModel(
        sale_order__name=sale_order__name,
        sale_order__sent_BGL=optional_fields["sale_order__sent_BGL"],
        sale_order__sent_Flex=optional_fields["sale_order__sent_Flex"],
        sale_order__sent_Hapro=optional_fields["sale_order__sent_Hapro"],
        sale_order__customer_ref=optional_fields["sale_order__customer_ref"],
        sale_order_line__name=optional_fields["sale_order_line__name"],
        sale_order_line__quantity=optional_fields["sale_order_line__quantity"],
        sale_order_line__price_unit=optional_fields["sale_order_line__price_unit"],
        sale_order__tracking_no=optional_fields["sale_order__tracking_no"],
        # sale_order__tracking_no_flex=optional_fields["sale_order__tracking_no_flex"],
        res_partner__huddly_customer=custAddress,
    )
