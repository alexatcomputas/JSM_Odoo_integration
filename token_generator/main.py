import logging

import functions_framework
import google.auth
import google.cloud.logging
from flask import Request

from environment import ENVIRONMENT, PROD_AUDIENCE, STAGE_AUDIENCE
from functions import BadPasswordException, create_id_token, get_credentials, get_current_project_id, validate_pass

if ENVIRONMENT == "local":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    logging.info("### Local environment detected ###")
else:
    logging.basicConfig(level=logging.INFO, format="%(name)s - %(levelname)s - %(message)s")
    logging.info("### Non-local environment detected ###")

current_project_id = get_current_project_id()


@functions_framework.http
def main(request: Request):
    password = None
    environment = None
    credentials = None
    token = None

    logging.info("Request received, starting up...")

    try:
        password = request.headers.get("password", None)
        environment = request.headers.get("environment", None)

        if password:
            validate_pass(password)
        else:
            logging.info("No password provided")
            raise BadPasswordException("No password")

        if ENVIRONMENT == "local":
            scopes = ["https://www.googleapis.com/auth/cloud-platform"]
            credentials, _ = google.auth.default(scopes=scopes)

        else:
            credentials = get_credentials(environment)

        if not credentials:
            logging.warning("Failed attaining credentials")
            raise Exception("Failed attaining credentials")

        token = create_id_token(credentials, environment)

        if not token:
            logging.error("Failed creating token")
            raise Exception("Failed creating token")

    except Exception as e:
        logging.error(f"Error: {e}")
        return ("Error getting token or credentials", 500)

    return (token, 200)


if __name__ == "__main__":
    main()
