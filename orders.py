import logging

from odoorpc import ODOO

from models import SaleOrder, SaleOrderLine, StockMoveLine, StockPicking
from services.odoo import Odoo

# logger = logging.getLogger("odoorpc")

# stock_move_line_model = odoo.env["stock.move.line"]
# picking_model = odoo.env["stock.picking"]
# sale_order_model = odoo.env["sale.order"]
# order_line_model = odoo.env["sale.order.line"]
# partner_model = odoo.env["res.partner"]


class GetOrders:
    def __init__(self, odoo: ODOO, serial_number: str):
        self.odoo = odoo
        self.stock_move_line_model = odoo.env["stock.move.line"]
        self.picking_model = odoo.env["stock.picking"]
        self.sale_order_model = odoo.env["sale.order"]
        self.order_line_model = odoo.env["sale.order.line"]

        # Initialize instance attributes to store data
        self.serial_number = serial_number
        self.lot_id = None
        self.picking_id = None
        self.sale_id = None
        self.stockpicking = None
        self.so_line = None
        self.sale_order = None

    def get_order_data(self) -> None:
        self.lot_id = self._search_lot_for_sns(self.serial_number)
        self.picking_id = self.lot_id[0].picking_id[0]

        self.stockpicking = self._get_StockPicking(self.picking_id)
        self.sale_id = self.stockpicking.sale_id[0]

        self.so_line = self._get_SO_line(order_line_id=self.sale_id)
        self.sale_order = self._get_sale_order(order_id=self.sale_id)

    def extract_order_data(self) -> dict:
        # Define types of requests

        pass

    def _search_lot_for_sns(self, lot_name_to_search: str) -> list[StockMoveLine]:
        model = self.stock_move_line_model
        matching_records_ids = model.search([("lot_name", "like", lot_name_to_search)])

        if matching_records_ids:
            records_data = model.read(
                matching_records_ids, ["lot_name", "product_id", "picking_id", "state", "origin"]
            )

        else:
            logging.info("No records found in stock.move.line with the specified lot name.")
            return []

        results = []
        # Process the data as needed
        for record in records_data:
            SML_instance = StockMoveLine(
                lot_name=record["lot_name"],
                product_id=record["product_id"],
                picking_id=record["picking_id"],
                state=record["state"],
                origin=record["origin"],
            )

            results.append(SML_instance)
            logging.info(f"Product ID: {SML_instance.product_id[0]}, Picking ID: {SML_instance.picking_id[0]} found")

        return results

    def _get_StockPicking(self, picking_id: int):
        model = self.picking_model
        picking_record = model.search([("id", "=", picking_id)])
        # Read the 'sale_id' field from the stock.picking record

        if picking_record:
            picking_data = model.read(picking_record, ["sale_id"])
            sale_id = picking_data[0].get("sale_id", None)
            if sale_id:
                logging.info(f"Sale ID: {sale_id[0]}")
                return StockPicking(id=picking_id, sale_id=sale_id)

        logging.warning("No stock.picking sale_id record found for the given picking_id {picking_id}")
        return StockPicking(id=-1, sale_id=-1)

    def _get_SO_line(self, order_line_id: int):
        model = self.order_line_model
        order_line_record = model.search([("id", "=", order_line_id)])

        if not order_line_record:
            logging.warning(f"Order line {order_line_id} not found.")
            return SaleOrderLine(id=-1, order_line_id=-1, product_id=-1)

        order_line_data = model.read(
            order_line_record, ["order_id", "product_id", "name", "product_uom_qty", "price_unit"]
        )

        if order_line_data:
            logging.info(f"Order line {order_line_id} found")

            order_line_record = order_line_data[0]
            order_line_data = SaleOrderLine(
                id=order_line_record.get("id", None),
                order_id=order_line_record.get("order_id", None),
                product_id=order_line_record.get("product_id", None),
                name=order_line_record.get("name", None),
                quantity=order_line_record.get("product_uom_qty", None),
                price_unit=order_line_record.get("price_unit", None),
            )

        return order_line_data

    def _get_sale_order(self, order_id: int):
        model = self.sale_order_model
        sale_order_record = model.search([("id", "=", order_id)])

        if not sale_order_record:
            logging.warning(f"Order {order_id} not found.")
            return SaleOrder(id=-1, order_id=-1, product_id=-1)

        sale_order_data = model.read(
            sale_order_record,
            [
                "name",  # Order reference
                "x_received_shipment",  # Sent from Hapro
                "delivered_date",  # Sent from Flex
                "sent_from_bgl_date",  # Sent from BGL
                "client_order_ref",  # Customer ref
                "soform_tracking_no",  # Tracking no
                "x_transporter_trackingno",  # Tracking no Flex
                "partner_id",  # Customer id
            ],
        )

        if sale_order_data:
            logging.info(f"Sale ordr {order_id} found, ")

            sale_orer_record = sale_order_data[0]
            sale_order_data = SaleOrder(
                id=sale_orer_record.get("id", None),
                name=sale_orer_record.get("name", None),
                sent_Hapro=sale_orer_record.get("x_received_shipment", None),
                sent_Flex=sale_orer_record.get("delivered_date", None),
                sent_BGL=sale_orer_record.get("sent_from_bgl_date", None),
                customer_ref=sale_orer_record.get("client_order_ref", None),
                tracking_no=sale_orer_record.get("soform_tracking_no", None),
                tracking_no_flex=sale_orer_record.get("x_transporter_trackingno", None),
                partner_id=sale_orer_record.get("partner_id", None),
            )

            return sale_order_data
