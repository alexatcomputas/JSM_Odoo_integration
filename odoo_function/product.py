from models import Product


class ProductParser:
    def __init__(self, customer_id):
        self.customer_id = customer_id
        self.product_data = self.fetch_product_data()

    def fetch_product_data(self) -> Product:
        serial_numbers = self._get_serial_numbers(self.customer_id)

        product = Product(
            
        )
        return



    def _get_serial_numbers(self) -> list[str]:
        return None

    def _get_

    # name: Annotated[str, StringConstraints(strip_whitespace=True)]
    # description: Annotated[str, StringConstraints(strip_whitespace=True)]
    # serial_numbers: Optional[list[Annotated[str, StringConstraints(strip_whitespace=True)]]]
    # list_price: Optional[float]
