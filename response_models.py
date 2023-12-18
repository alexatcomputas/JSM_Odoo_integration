from typing import Annotated, Optional, Union

from pydantic import BaseModel, Field, StringConstraints

StrAnnotated = Annotated[str, StringConstraints(strip_whitespace=True)]
StrAnnotatedorFalse = Optional[Union[str, bool, Annotated[str, StringConstraints(strip_whitespace=True)]]]
ListIntStr = list[Union[int, StrAnnotated]]
ListIntStrorBool = Union[ListIntStr, bool]


class returnModel(BaseModel):
    sale_order__name: StrAnnotated = Field(serialization_alias="SalesOrdernumber", example="SO4312")
    sale_order__sent_BGL: Optional[StrAnnotated] = Field(
        serialization_alias="SentfromdatefromBGL", example="2021-08-31 13:02:44", default=None
    )
    sale_order__sent_Flex: Optional[StrAnnotated] = Field(
        serialization_alias="SentfromdatefromFlex", example="2021-08-31 13:02:44", default=None
    )
    sale_order__sent_Hapro: Optional[StrAnnotated] = Field(
        serialization_alias="SentfromdatefromHapro", example="2021-08-31 13:02:44", default=None
    )
    sale_order__customer_ref: Optional[StrAnnotated] = Field(
        serialization_alias="Customerreference", example="550", default=None
    )
    sale_order_line__name: Optional[StrAnnotated] = Field(
        serialization_alias="Productdescription",
        example="[7090043790672] Huddly L1 Kit incl. USB Adapter...",
        default=None,
    )
    sale_order_line__quantity: Optional[float] = Field(
        serialization_alias="Orderedquantity", example="8.0", default=None
    )
    sale_order_line__price_unit: Optional[float] = Field(
        serialization_alias="Unitprice", example="960.0", default=None
    )
    sale_order__tracking_no: Optional[StrAnnotated] = Field(serialization_alias="Trackingnumber", default=None)
    # sale_order__tracking_no_flex: Optional[Union[StrAnnotated, int]] = Field(
    #     serialization_alias="trackingno_flex")  # Needs field ID to work
    res_partner__huddly_customer: Optional[str] = Field(
        serialization_alias="Huddlycustomer", example="Customer name + address", default=None
    )


# class BaseResponseModel(BaseModel):
#     return_code: int
#     message: str


# class OrderResponseModel(BaseResponseModel):
#     data: returnModelOrder


# class CustomerResponseModel(BaseResponseModel):
#     data: returnModelCustomer


###

# cust = returnModelCustomer(res_partner__huddly_customer="test cust address", res_partner__huddly_customer2=None)
# print(cust.model_dump_json(by_alias=True, exclude_none=True))
