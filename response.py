from abc import ABC, abstractmethod

from flask import Flask, jsonify, request

from models import Type1ResponseModel


class ResponseBuilder(ABC):
    @abstractmethod
    def build_response(self, data):
        pass


class Type1ResponseBuilder(ResponseBuilder):
    def build_response(self, data):
        return Type1ResponseModel(success=True, message="Type 1 response", data=data)


# Factory
def get_response_builder(request_type):
    if request_type == "type1":
        return Type1ResponseBuilder()
    else:
        raise ValueError("Unknown request type")
