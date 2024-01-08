import json

from flask import jsonify, request

from response_models import ResponseModel


def dump_request():
    log_message = (
        f"Method: {request.method}\n"
        f"URL: {request.url}\n"
        f"Headers: {request.headers}\n"
        f"Body: {request.get_data(as_text=True)}\n"
        f"Args: {request.args}\n"
        f"Form: {request.form}"
    )
    return log_message


def process_and_jsonify_input(input_data):
    """
    Processes the input data which can be either an instance of ResponseModel or a plain string.
    Returns a Flask Response object with application/json mimetype.

    :param input_data: An instance of ResponseModel or a plain text string.
    :return: Flask Response object with the input converted to JSON.
    """
    if isinstance(input_data, ResponseModel):
        # Serialize the ResponseModel instance
        serialized_data = input_data.model_dump_json(by_alias=True, exclude_none=False)
        data_dict = json.loads(serialized_data)

        # Add the message to the response
        data_dict["message"] = "Serial number found"
        return jsonify(data_dict)

    else:
        # If input is a plain string, jsonify it directly with a message
        return jsonify({"message": input_data})
