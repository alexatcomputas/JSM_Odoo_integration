import logging
from types import SimpleNamespace

from odoorpc import ODOO

from models import SaleOrder, SaleOrderLine, StockMoveLine, StockPicking
from product import Products


class Order:
    def __init__(self, odoo: ODOO, serial_number: str):
        self.odoo = odoo
        self.stock_move_line_model = odoo.env["stock.move.line"]
        self.production_lot_model = odoo.env["stock.production.lot"]
        self.picking_model = odoo.env["stock.picking"]
        self.sale_order_model = odoo.env["sale.order"]
        self.order_line_model = odoo.env["sale.order.line"]
        self.error_models = SimpleNamespace()
        self.error_models.stockmoveline = StockMoveLine(lot_name="-1", product_id=[-1, ""], picking_id=[-1, ""])
        self.error_models.stockpicking = StockPicking(id=-1, sale_id=[-1, ""])
        self.error_models.saleorderline = SaleOrderLine(id=-1, order_id=-1, product_id=-1)
        self.error_models.saleorder = SaleOrder(id=-1, name="")

        # Initialize instance attributes to store data
        self.serial_number = serial_number
        self.stockmoveline = None
        self.picking_ids = []
        self.product_ids = []
        self.sale_id = None
        self.stockpicking = None
        self.products = []
        self.so_line = None
        self.sale_order = None

    def get_order_data(self) -> None:
        # Search for records in 'stock.move.line'
        self.stockmoveline = self.get_stockmoveline(self.serial_number)

        if self.stockmoveline == self.error_models.stockmoveline:
            logging.warning(f"No records found in 'stock.move.line' with the specified serial number/lot name: [{self.serial_number}].")
            logging.warning("Returning 404")
            return

        # Get the picking id's. Ignore items with picking_id False
        for item in self.stockmoveline:
            if item.picking_id:
                self.picking_ids.append(item.picking_id[0])
            if item.product_id:
                self.product_ids.append(item.product_id[0])

        # TODO: Get the product name for the product_id which has more than one serial number
        for item in self.stockmoveline:
            # split lot_name string by comma into temp list
            lotnames = item.lot_name.split(",")
            if len(lotnames) > 1:
                self.products = Products(product_ids=item.product_id[0])
                break
            else:
                self.products = self.products.append(Products(product_ids=item.product_id[0]))

        # Proceed if picking id's are found, else exit
        if self.picking_ids:
            temp_picking_ids = self.picking_ids.copy()
            for picking_id in self.picking_ids:
                self.stockpicking = self.get_StockPicking(picking_id)
                if self.stockpicking == self.error_models.stockpicking:
                    temp_picking_ids.pop(temp_picking_ids.index(picking_id))
                    logging.warning(
                        f"""No stock.picking sale_id record found for the given picking_id {picking_id}.
                                    Continuing to search with the rest of the records [{temp_picking_ids}]"""
                    )
        else:
            logging.warning(f"No picking ids found with the specified serial number/lot name: [{self.serial_number}].")
            logging.warning("Returning 404")
            raise ValueError(f"No picking ids found with the specified serial number/lot name: [{self.serial_number}].")

        self.sale_id = self.stockpicking.sale_id[0]
        self.sale_order = self.get_sale_order(order_id=self.sale_id)

        # Get sale order line, if multiple products: Check them all and return the one which has "Kit" in its name
        # If no "Kit" Item, concatenate all names.
        so_line_items = []
        for product_id in self.product_ids:
            so_line_item = self.get_SaleOrderLine(order_id=self.sale_id, product_id=product_id)
            if so_line_item and so_line_item != self.error_models.saleorderline:
                so_line_items.append(so_line_item)

        # Check that the product name contains "Kit"
        # for so_line_item in so_line_items:
        #     if "Kit" in so_line_item.name:
        #         self.so_line = so_line_item
        #         break

        if not self.so_line:
            self.so_line = so_line_items

        if not self.so_line:
            raise ValueError(f"No sale order line found for product {self.sale_id}")

    def create_odoo_filters(self, field_name: str, lot_ids: list[str]) -> list:
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

    def search_stock_move_line(self, lot_ids: list[str]):
        filters = self.create_odoo_filters("lot_name", lot_ids)
        return self.stock_move_line_model.search(filters)

    def _search_production_lot(self, lot_ids: list[str]):
        filters = self.create_odoo_filters("name", lot_ids)
        lot_records = self.production_lot_model.search_read(filters)

        if lot_records:
            filters = [("lot_id", "=", lot_records[0]["id"])]
            return self.stock_move_line_model.search(filters)
        else:
            return []

    def create_stock_move_line(self, records_data) -> list[StockMoveLine]:
        # Logic to create StockMoveLine objects from records
        results = []
        for record in records_data:
            stockmoveline = StockMoveLine(
                lot_name=record.get("lot_name", None),
                product_id=record.get("product_id", None),
                picking_id=record.get("picking_id", None),
                state=record.get("state", None),
                origin=record.get("origin", None),
                company_id=record.get("company_id", None),
            )

            results.append(stockmoveline)

            product_id = getattr(stockmoveline, "product_id", None)
            picking_id = getattr(stockmoveline, "picking_id", None)
            logging.info(f"Product ID: {product_id}, Picking ID: {picking_id}")

        return results

    def get_stockmoveline(self, lot_name_to_search: str) -> list[StockMoveLine]:
        error_model = self.error_models.stockmoveline
        lot_ids = lot_name_to_search.replace(" ", "").split(",")

        matching_record_ids = self.search_stock_move_line(lot_ids)

        if not matching_record_ids:
            logging.info("No records found in stock.move.line with the specified lot name. Checking production.lot for lot reference.")
            matching_record_ids = self._search_production_lot(lot_ids)
            if not matching_record_ids:
                logging.warning(f"No production.lot record found either for lot id's [{', '.join(lot_ids)}].")

        if not matching_record_ids:
            logging.info(
                f"""Could not find any matching record data in stock.move.line/production lot with
                specified lot name/serial number [{lot_name_to_search}]."""
            )
            return error_model

        records_data = self.stock_move_line_model.read(
            matching_record_ids, ["lot_name", "product_id", "picking_id", "state", "origin", "company_id"]
        )

        stockmoveline = self.create_stock_move_line(records_data)
        return stockmoveline

    def get_StockPicking(self, picking_id: int) -> StockPicking:
        model = self.picking_model
        error_model = self.error_models.stockpicking

        picking_record = model.search([("id", "=", picking_id)])
        # Read the 'sale_id' field from the stock.picking record

        if picking_record:
            picking_data = model.read(picking_record, ["sale_id"])
            sale_id = picking_data[0].get("sale_id", None)
            if sale_id:
                logging.info(f"Sale ID: {sale_id[0]}")
                return StockPicking(id=picking_id, sale_id=sale_id)

        logging.warning(f"No stock.picking sale_id record found for the given picking_id {picking_id}")
        return error_model

    def get_SaleOrderLine(self, order_id: int, product_id: int) -> SaleOrderLine:
        model = self.order_line_model
        error_model = self.error_models.saleorderline

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
            return error_model

    def get_sale_order(self, order_id: int):
        model = self.sale_order_model
        error_model = self.error_models.saleorder

        sale_order_record = model.search([("id", "=", order_id)])

        if not sale_order_record:
            logging.warning(f"Order {order_id} not found.")
            return error_model

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

    def get_product():
        pass
