from typing import Annotated, Optional, Union

from pydantic import BaseModel, EmailStr, StringConstraints

StrAnnotated = Annotated[str, StringConstraints(strip_whitespace=True)]
StrAnnotatedorFalse = Optional[Union[str, bool, Annotated[str, StringConstraints(strip_whitespace=True)]]]
ListIntStr = list[Union[int, StrAnnotated]]
ListIntStrorBool = Union[ListIntStr, bool]


# Table: stock.move.line
class StockMoveLine(BaseModel):
    lot_name: StrAnnotatedorFalse
    product_id: ListIntStr
    picking_id: ListIntStrorBool
    state: Optional[StrAnnotated] = None
    origin: Optional[StrAnnotated] = None
    company_id: Optional[ListIntStr] = None


# Table: res.partner
class Customer(BaseModel):
    id: int
    email: Optional[EmailStr] = None
    name: Optional[StrAnnotatedorFalse] = None
    street: Optional[StrAnnotatedorFalse] = None
    city: Optional[StrAnnotatedorFalse] = None
    postal_code: Optional[StrAnnotatedorFalse] = None
    state: Optional[ListIntStrorBool] = None
    country: Optional[ListIntStrorBool] = None
    customer_reference: Optional[StrAnnotatedorFalse] = None
    is_company: Optional[bool] = None


# Table: stock.picking
class StockPicking(BaseModel):
    id: int
    sale_id: ListIntStr


# Table: sale.order
class SaleOrder(BaseModel):
    id: int
    name: StrAnnotated
    sent_Hapro: Optional[StrAnnotatedorFalse] = None
    sent_Flex: Optional[StrAnnotatedorFalse] = None
    sent_BGL: Optional[StrAnnotatedorFalse] = None
    customer_ref: Optional[StrAnnotatedorFalse] = None
    tracking_no: Optional[StrAnnotatedorFalse] = None
    tracking_no_flex: Optional[StrAnnotatedorFalse] = None
    partner_id: Optional[ListIntStr] = None


# Table: sale.order.line
class SaleOrderLine(BaseModel):
    id: int
    order_id: int
    product_id: int
    name: Optional[StrAnnotated] = None
    quantity: Optional[float] = None
    price_unit: Optional[float] = None


class Product(BaseModel):
    id: int
    name: Optional[StrAnnotated] = None
    barcode: Optional[StrAnnotated] = None
    # alternative_barcodes: Optional[StrAnnotated] = None
