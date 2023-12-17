from customer import GetCustomer
from orders import GetOrders
from response_models import returnModelCustomer, returnModelOrder


def buildOrderResponse(Order: GetOrders) -> returnModelOrder:
    pass


def buildCustomerResponse(Customer: GetCustomer) -> returnModelCustomer:
    Customer.buildCustomerField()
    print(Customer.return_item)
    print("")


# from abc import ABC, abstractmethod

# from models import Type1ResponseModel
# from response_models import returnModelCustomer, returnModelOrder

# class ResponseBuilder(ABC):
#     @abstractmethod
#     def build_response(self, data):
#         pass


# class Type1ResponseBuilder(ResponseBuilder):
#     def build_response(self, data):
#         return Type1ResponseModel(success=True, message="Type 1 response", data=data)


# # Factory
# def get_response_builder(request_type):
#     if request_type == "type1":
#         return Type1ResponseBuilder()
#     else:
#         raise ValueError("Unknown request type")


# customerResponseData = returnModelCustomer(res_partner__huddly_customer=buildCustomerField(Customer))
# print(cust.model_dump_json(by_alias=True, exclude_none=True))
