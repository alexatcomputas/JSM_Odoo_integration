import json
import logging
import os
import time
from typing import Optional, Tuple

import requests
from google.auth import default, jwt
from google.oauth2 import service_account

from environment import PASS_FASIT, PROD_AUDIENCE, STAGE_AUDIENCE

audience = {"PROD": PROD_AUDIENCE, "STAGE": STAGE_AUDIENCE}


class BadPasswordException(Exception):
    def __init__(self, password, message="Password is incorrect"):
        self.password = password
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f"{self.message} -> {self.password}"


def validate_pass(password) -> bool:
    """
    Evaluate the password.
    """
    if password == PASS_FASIT:
        logging.info("Password is correct")
        return True
    else:
        logging.info(f"Password is incorrect.")
        raise BadPasswordException(password)


def get_current_project_id() -> Tuple[any, Optional[str]]:
    """
    Retrieve the current GCP project ID.
    """
    _, project_id = default()
    if project_id is None:
        raise Exception("Project ID could not be determined.")

    return project_id


def get_credentials(env: str) -> service_account.Credentials:
    if env:
        logging.info("Getting credentials from env")
        ENV = env.upper()
        credentials_str = os.environ.get(f"{ENV}_CREDENTIALS")

    if not credentials_str:
        logging.warning(f"Getting credentials failed, env = {env}")
        raise Exception("Credentials not found/Env variable not set")

    credentials_info = json.loads(credentials_str)

    credentials = service_account.Credentials.from_service_account_info(
        credentials_info, scopes=["https://www.googleapis.com/auth/cloud-platform"]
    )

    return credentials


def create_id_token(credentials, environment: str = "STAGE", aud: dict = audience):
    """
    Create a Google-signed ID token from the provided service account credentials.
    """
    if not credentials:
        raise Exception("Credentials missing in create_token_from_credentials")

    env = environment.upper()
    if env not in aud:
        raise Exception(f"Invalid environment, cant map {env} to key in audience dict")

    # if credentials.requires_scopes:
    credentials = credentials.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])

    audience_url = aud[env]

    signed_jwt = jwt.encode(
        credentials.signer,
        {
            "aud": "https://oauth2.googleapis.com/token",
            "iss": credentials.service_account_email,
            "target_audience": audience_url,
            "exp": int(time.time()) + 120,  # GCP ID token still has 1h expiry so this is kinda misleading "¯\_(ツ)_/¯ "
            "iat": int(time.time()),
        },
    )

    # Exchange the JWT for an ID token
    response = requests.post(
        "https://oauth2.googleapis.com/token",
        data={"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": signed_jwt},
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    if response:
        if response.status_code == 200:
            logging.info(f"Response: 200 - SUCCESS")
        else:
            logging.error(f"Response: Failed: {response.status_code}")
            # logging.debug(f"Response: {response.status_code} {response.text}")
    else:
        logging.error("JWT Request failed")

    response_data = response.json()

    return response_data["id_token"]
