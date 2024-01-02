from flask import request


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
