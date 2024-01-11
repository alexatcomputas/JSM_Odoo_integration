from types import SimpleNamespace

from odoorpc import ODOO

from models import Product
from odoo import Odoo as odoo


class Products:
    def __init__(self, product_ids: list[int] = None, barcodes: list[str] = None, odoo: ODOO = odoo):
        self.odoo = odoo
        self.product_model = odoo.env["product.product"]
        self.error_models = SimpleNamespace()
        self.error_models.product = Product(id="-1", name="-1", barcode="-1")
        self.products = self.get_products(product_ids, barcodes=barcodes)

    def get_all_products(self) -> list[Product]:
        # Search by id if not None. Search by barcode if not None, if both have values do both and concatenate results
        return self.products

    def get_products(self, product_ids: list[int] = None, barcodes: list[str] = None) -> list[Product]:
        products = []

        if product_ids:
            products.extend(self._get_product_by_id(product_ids))

        if barcodes:
            products.extend(self._get_product_by_barcode(barcodes))

        return products

    def _get_product_by_id(self, product_ids: list[int]) -> Product:
        products = []

        results = self.product_model.read(product_ids, ["id", "name", "barcode"])

        for record in results:
            product = Product(
                id=record.get("id", None),
                name=record.get("name", None),
                barcode=record.get("barcode", None),
            )

            products.append(product)

        return products

    def _get_product_by_barcode(self, barcodes: list[str]) -> Product:
        products = []
        product_ids = self.product_model.search([("barcode", "=", barcodes)])

        if not product_ids:
            return products

        results = self.product_model.read(product_ids, ["id", "name", "barcode"])

        for record in results:
            product = Product(
                id=record.get("id", None),
                name=record.get("name", None),
                barcode=record.get("barcode", None),
            )

            products.append(product)

        return products
