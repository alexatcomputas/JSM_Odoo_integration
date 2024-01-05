from types import SimpleNamespace

from odoorpc import ODOO

from models import Product
from odoo import Odoo as odoo

# class ProductParser:
#     def __init__(self, customer_id):
#         self.customer_id = customer_id
#         self.product_data = self.fetch_product_data()

#     def fetch_product_data(self) -> Product:
#         serial_numbers = self._get_serial_numbers(self.customer_id)

#         product = Product()
#         return

#     def _get_serial_numbers(self) -> list[str]:
#         return None

#     # def _get_

#     # name: Annotated[str, StringConstraints(strip_whitespace=True)]
#     # description: Annotated[str, StringConstraints(strip_whitespace=True)]
#     # serial_numbers: Optional[list[Annotated[str, StringConstraints(strip_whitespace=True)]]]
#     # list_price: Optional[float]


# Access the product model
# product_model = odoo.env["product.product"]

# Barcode retrieved from stock.move.line
# barcode = "7090043790672"
# barcode = "7090043790948"

# Search for the product using the barcode
# product_ids = product_model.search([("barcode", "=", barcode)])

# Search for products
# product_ids = Product.search([])
# product_ids = [333]
# product_ids = [290, 293]

# Read the products' data
# products = product_model.read(product_ids, ["name", "barcode"])


class Products:
    def __init__(self, product_ids: list[int] = None, barcodes: list[str] = None, odoo: ODOO = odoo):
        self.odoo = odoo
        self.product_model = odoo.env["product.product"]
        self.error_models = SimpleNamespace()
        self.error_models.product = Product(id="-1", name="-1", barcode="-1")
        self.products = self.get_products(product_ids, barcodes=barcodes)

    def get_all_products(self) -> list[Product]:
        # Search by id if it is not None, either search by barcode if it is not None, if both have values do both and concatenate results
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


products = Products(product_ids=[260, 271, 263], barcodes=["7090043790672"])
