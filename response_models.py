from pydantic import BaseModel


class BaseResponseModel(BaseModel):
    success: bool
    message: str


class Type1ResponseModel(BaseResponseModel):
    data: dict


# class Type2ResponseModel(BaseResponseModel):
#     items: list
