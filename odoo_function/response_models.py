from typing import Annotated, Optional, Union

from pydantic import BaseModel, Field, StringConstraints

StrAnnotated = Annotated[str, StringConstraints(strip_whitespace=True)]
StrAnnotatedorFalse = Optional[Union[str, bool, Annotated[str, StringConstraints(strip_whitespace=True)]]]
ListIntStr = list[Union[int, StrAnnotated]]
ListIntStrorBool = Union[ListIntStr, bool]


class ResponseModel(BaseModel):
    sale_order__name: StrAnnotated = Field(serialization_alias="SalesOrdernumber", example="SO4312")
    sale_order__sent_BGL: Optional[StrAnnotated] = Field(
        serialization_alias="SentfromdatefromBGL", example="2021-08-31 13:02:44", default=None
    )
    sale_order__sent_Flex: Optional[StrAnnotated] = Field(
        serialization_alias="SentfromdatefromFlex", example="2021-08-31 13:02:44", default=""
    )
    sale_order__sent_Hapro: Optional[StrAnnotated] = Field(
        serialization_alias="SentfromdatefromHapro", example="2021-08-31 13:02:44", default=""
    )
    sale_order__customer_ref: Optional[StrAnnotated] = Field(serialization_alias="Customerreference", example="550", default=None)
    sale_order_line__name: Optional[StrAnnotated] = Field(
        serialization_alias="Productdescription2",
        example="[7090043790672] Huddly L1 Kit incl. USB Adapter...",
        default=None,
    )
    product_product__name: Optional[StrAnnotated] = Field(serialization_alias="Productdescription", example="Huddly L1 Kit", default=None)
    sale_order_line__quantity: Optional[float] = Field(serialization_alias="Orderedquantity", example="8.0", default=None)
    sale_order_line__price_unit: Optional[float] = Field(serialization_alias="Unitprice", example="960.0", default=None)
    sale_order__tracking_no: Optional[StrAnnotated] = Field(serialization_alias="Trackingnumber", default=None)
    # sale_order__tracking_no_flex: Optional[Union[StrAnnotated, int]] = Field(
    #     serialization_alias="trackingno_flex")
    res_partner__name: Optional[StrAnnotated] = Field(serialization_alias="Customer", example="Customer name", default=None)
    res_partner__street: Optional[StrAnnotated] = Field(serialization_alias="StreetAddress", example="Street", default=None)
    res_partner__city: Optional[StrAnnotated] = Field(serialization_alias="City", example="City", default=None)
    res_partner__postal_code: Optional[StrAnnotated] = Field(serialization_alias="PostalCode", example="90120", default=None)
    res_partner__state: Optional[StrAnnotated] = Field(serialization_alias="State", example="OSLO", default=None)
    res_partner__country: Optional[StrAnnotated] = Field(serialization_alias="Country", example="NORWAY", default=None)
