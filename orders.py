import logging

from odoorpc import ODOO

from models import SaleOrder, SaleOrderLine, StockMoveLine, StockPicking


class Order:
    def __init__(self, odoo: ODOO, serial_number: str):
        self.odoo = odoo
        self.production_lot_model = odoo.env["stock.production.lot"]
        self.stock_move_line_model = odoo.env["stock.move.line"]
        self.picking_model = odoo.env["stock.picking"]
        self.sale_order_model = odoo.env["sale.order"]
        self.order_line_model = odoo.env["sale.order.line"]

        # Initialize instance attributes to store data
        self.serial_number = serial_number
        self.stockmoveline = None
        self.picking_id = None
        self.product_id = None
        self.sale_id = None
        self.stockpicking = None
        self.so_line = None
        self.sale_order = None

    def get_order_data(self) -> None:
        # Search for records in 'stock.move.line'
        self.stockmoveline = self._get_stockmoveline(self.serial_number)

        if self.stockmoveline.lot_name == "-1":
            logging.warning(
                f"""No records found in 'stock.move.line'
                with the specified serial number/lot name: [{self.serial_number}].
                """
            )
            return
        # Get the picking id's. Ignore items with False
        self.picking_id = self.stockmoveline.picking_id[0] if self.stockmoveline.picking_id else None
        self.product_id = self.stockmoveline.product_id[0] if self.stockmoveline.product_id else None

        self.stockpicking = self._get_StockPicking(self.picking_id)
        self.sale_id = self.stockpicking.sale_id[0]

        self.so_line = self._get_SaleOrderLine(order_id=self.sale_id, product_id=self.product_id)
        self.sale_order = self._get_sale_order(order_id=self.sale_id)

    def _get_stockmoveline(self, lot_name_to_search: str) -> StockMoveLine:
        model = self.stock_move_line_model
        error_model = StockMoveLine(lot_name="-1", product_id=[-1, ""], picking_id=False)

        # Remove all spaces and split the lot_name_to_search into a list of names
        lot_ids = lot_name_to_search.replace(" ", "").split(",")

        def _create_odoo_filters(field_name, lot_ids):
            # Initialize filters with the company condition
            filters = [("company_id", "=", 1)]
            lot_id_filters = []

            # Check if there is exactly one lot_id
            if len(lot_ids) == 1:
                # Add it to the filters with an implicit AND clause
                filters.append((field_name, "ilike", lot_ids[0]))
            else:
                # If there's more than one lot_id, prepare for OR logic
                for lot_id in lot_ids:
                    lot_id_filters.append((field_name, "ilike", lot_id))

                # Finally, Add the lot_id filters to the filters list with OR logic
                if lot_id_filters:
                    filters.append("|")
                    filters.extend(lot_id_filters)

            return filters

        filters = _create_odoo_filters("lot_name", lot_ids)
        matching_record_ids = model.search(filters)

        # If no records found in stock.move.line, perform alternative approach:
        # check for a lot reference in production.lot.name instead
        if not matching_record_ids:
            logging.info("No records found in stock.move.line with the specified lot name. Checking production.lot for lot reference.")

            filters = _create_odoo_filters("name", lot_ids)
            lot_records = self.production_lot_model.search_read(filters)

            if lot_records:
                filters = [("lot_id", "=", lot_records[0]["id"])]
                matching_record_ids = model.search(filters)
            else:
                logging.warning(f"No production.lot record found either for serial number {lot_name_to_search}. Exiting.")
                return error_model

        if not matching_record_ids:
            logging.info(f"Error retrieving data in stock.move.line with specified lot name/serial number [{lot_name_to_search}].")
            return error_model

        if matching_record_ids:
            records_data = model.read(matching_record_ids, ["lot_name", "product_id", "picking_id", "state", "origin", "company_id"])

        # results = []
        for record in records_data:
            if record["picking_id"]:
                stockmoveline = StockMoveLine(
                    lot_name=record.get("lot_name", None),
                    product_id=record.get("product_id", None),
                    picking_id=record.get("picking_id", None),
                    state=record.get("state", None),
                    origin=record.get("origin", None),
                    company_id=record.get("company_id", None),
                )

                # results.append(stockmoveline)
                logging.info(f"Product ID: {stockmoveline.product_id}, Picking ID: {stockmoveline.picking_id}")
                break

        return stockmoveline

    def _get_StockPicking(self, picking_id: int) -> StockPicking:
        model = self.picking_model
        picking_record = model.search([("id", "=", picking_id)])
        # Read the 'sale_id' field from the stock.picking record

        if picking_record:
            picking_data = model.read(picking_record, ["sale_id"])
            sale_id = picking_data[0].get("sale_id", None)
            if sale_id:
                logging.info(f"Sale ID: {sale_id[0]}")
                return StockPicking(id=picking_id, sale_id=sale_id)

        logging.warning(f"No stock.picking sale_id record found for the given picking_id {picking_id}")
        return StockPicking(id=-1, sale_id=-1)

    def _get_SaleOrderLine(self, order_id: int, product_id: int) -> SaleOrderLine:
        model = self.order_line_model

        matching_records_ids = model.search([("order_id", "=", order_id), ("product_id", "=", product_id)])

        if matching_records_ids:
            records_data = model.read(matching_records_ids, ["name", "product_uom_qty", "price_unit"])
            record = records_data[0]
            return SaleOrderLine(
                id=record["id"],
                order_id=order_id,
                product_id=product_id,
                name=record["name"],
                quantity=record["product_uom_qty"],
                price_unit=record["price_unit"],
            )

        else:
            logging.info("No records found in sale.order.line with the specified order_id and product_id.")
            return SaleOrderLine(id=-1, order_id=-1, product_id=-1)

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
            logging.info(f"Sale order {order_id} found, processing data...")

            sale_order_record = sale_order_data[0]
            sale_order_data = SaleOrder(
                id=sale_order_record.get("id", None),
                name=sale_order_record.get("name", None),
                sent_Hapro=sale_order_record.get("x_received_shipment", None),
                sent_Flex=sale_order_record.get("delivered_date", None),
                sent_BGL=sale_order_record.get("sent_from_bgl_date", None),
                customer_ref=sale_order_record.get("client_order_ref", None),
                tracking_no=sale_order_record.get("soform_tracking_no", None),
                tracking_no_flex=sale_order_record.get("x_transporter_trackingno", None),
                partner_id=sale_order_record.get("partner_id", None),
            )

            return sale_order_data
