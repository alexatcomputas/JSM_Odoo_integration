from typing import Annotated, Optional, Union

from pydantic import BaseModel, EmailStr, Field, StringConstraints

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
    email: EmailStr
    name: StrAnnotatedorFalse
    street: StrAnnotatedorFalse
    city: StrAnnotatedorFalse
    postal_code: StrAnnotatedorFalse
    state: ListIntStrorBool
    country: ListIntStrorBool
    customer_reference: StrAnnotatedorFalse
    is_company: Optional[bool] = None


# Table: stock.picking
class StockPicking(BaseModel):
    id: int
    sale_id: ListIntStr


# Table: sale.order
class SaleOrder(BaseModel):
    id: int
    name: StrAnnotated
    sent_Hapro: StrAnnotatedorFalse
    sent_Flex: StrAnnotatedorFalse
    sent_BGL: StrAnnotatedorFalse
    customer_ref: StrAnnotatedorFalse
    tracking_no: StrAnnotatedorFalse
    tracking_no_flex: StrAnnotatedorFalse
    partner_id: ListIntStr


# Table: sale.order.line
class SaleOrderLine(BaseModel):
    id: int
    order_id: int
    product_id: int
    name: Optional[StrAnnotated] = None
    quantity: Optional[float] = None
    price_unit: Optional[float] = None


# Return to JSM ####
# Request type:
# class Order(BaseModel):
#     order_id: StrAnnotated
#     order_type: StrAnnotated
#     product_id: int
#     serial_number: StrAnnotated
#     picking_id: int
#     name: Optional[StrAnnotated]
#     sent_hapro: StrAnnotated
#     sent_flex: StrAnnotated
#     sent_bgl: StrAnnotated
#     tracking: StrAnnotated
#     tracking_flex: StrAnnotated
#     customer: StrAnnotated
#     street: StrAnnotated
#     city: StrAnnotated
#     zip: StrAnnotated
#     state: StrAnnotated
#     country: StrAnnotated
#     customer_reference: StrAnnotated

#     quantity: Optional[float]
#     price_unit: Optional[float]


# TODO: REMOVE?
# class Sales_order(BaseModel):
#     id: int
#     # product: list[Product]
#     product: StrAnnotated
#     order_quantity: int
#     sender: StrAnnotated
#     sent_date: StrAnnotated
#     tracking_number: StrAnnotated


# TODO: Remove this model?
# Table:
# class Product(BaseModel):
#     id: int
#     name: StrAnnotated
#     description: StrAnnotatedorFalse
#     serial_numbers: Optional[ListIntStr]
#     list_price: Optional[float]
