from typing import Annotated, Optional, Union

from pydantic import BaseModel, EmailStr, StringConstraints, validator

ListorBool = Optional[Union[list, bool]]
StrAnnotated = Annotated[str, StringConstraints(strip_whitespace=True)]
StrAnnotatedorFalse = Optional[Union[str, bool, Annotated[str, StringConstraints(strip_whitespace=True)]]]


class Product(BaseModel):
    id: int
    name: StrAnnotated
    description: StrAnnotatedorFalse
    serial_numbers: Optional[list[Annotated[str, StringConstraints(strip_whitespace=True)]]]
    list_price: Optional[float]


class Sales_order(BaseModel):
    id: int
    # product: list[Product]
    product: StrAnnotated
    order_quantity: int
    sender: StrAnnotated
    sent_date: StrAnnotated
    tracking_number: StrAnnotated


class Customer(BaseModel):
    id: int
    email: EmailStr
    name: StrAnnotatedorFalse
    street: StrAnnotatedorFalse
    city: StrAnnotatedorFalse
    postal_code: StrAnnotatedorFalse
    state: StrAnnotatedorFalse
    country: ListorBool
    customer_reference: StrAnnotatedorFalse
    is_company: Optional[bool]


class StockMoveLine(BaseModel):
    lot_name: StrAnnotated
    product_id: list[Union[int, StrAnnotated]]
    picking_id: list[Union[int, StrAnnotated]]
    state: StrAnnotated
    origin: StrAnnotated


class StockPicking(BaseModel):
    id: int
    sale_id: list[Union[int, StrAnnotated]]


class SaleOrder(BaseModel):
    id: int
    name: StrAnnotated
    sent_Hapro: StrAnnotatedorFalse
    sent_Flex: StrAnnotatedorFalse
    sent_BGL: StrAnnotatedorFalse
    customer_ref: StrAnnotatedorFalse
    tracking_no: StrAnnotatedorFalse
    tracking_no_flex: StrAnnotatedorFalse
    partner_id: list[Union[int, StrAnnotated]]


class SaleOrderLine(BaseModel):
    id: int
    order_id: list[Union[int, StrAnnotated]]
    product_id: list[Union[int, StrAnnotated]]
    name: Optional[StrAnnotated]
    quantity: Optional[float]
    price_unit: Optional[float]


# class Order(BaseModel):
