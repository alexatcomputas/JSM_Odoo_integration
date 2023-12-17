from typing import Annotated, Optional, Union

from pydantic import BaseModel, Field, StringConstraints

StrAnnotated = Annotated[str, StringConstraints(strip_whitespace=True)]
StrAnnotatedorFalse = Optional[Union[str, bool, Annotated[str, StringConstraints(strip_whitespace=True)]]]
ListIntStr = list[Union[int, StrAnnotated]]
ListIntStrorBool = Union[ListIntStr, bool]

# from pydantic import ConfigDict
# model_config = ConfigDict(populate_by_name=True)


class returnModelOrder(BaseModel):
    sale_order__name: StrAnnotated = Field(serialization_alias="customfieldId_10562", example="SO4312")
    sale_order__sent_BGL: Optional[StrAnnotated] = Field(
        serialization_alias="customfieldId_10563", example="2021-08-31 13:02:44"
    )
    sale_order__sent_Flex: Optional[StrAnnotated] = Field(
        serialization_alias="customfieldId_10564", example="2021-08-31 13:02:44"
    )
    sale_order__sent_Hapro: Optional[StrAnnotated] = Field(
        serialization_alias="customfieldId_10565", example="2021-08-31 13:02:44"
    )
    sale_order__customer_ref: Optional[StrAnnotated] = Field(serialization_alias="customfieldId_10566", example="550")
    sale_order_line__name: Optional[StrAnnotated] = Field(
        serialization_alias="customfieldId_10567", example="[7090043790672] Huddly L1 Kit incl. USB Adapter..."
    )
    sale_order_line__quantity: Optional[float] = Field(serialization_alias="customfieldId_10568", example="8.0")
    sale_order_line__price_unit: Optional[StrAnnotated] = Field(
        serialization_alias="customfieldId_10569", example="960.0"
    )
    sale_order__tracking_no: Optional[StrAnnotated] = Field(serialization_alias="customfieldId_10570")


class returnModelCustomer(BaseModel):
    res_partner__huddly_customer: str = Field(
        serialization_alias="customfieldId_10571", example="Customer name + address"
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
