import os

from dotenv import load_dotenv

load_dotenv()
ENVIRONMENT = os.getenv("environment", default="cloud")
PASS_FASIT = os.getenv("access_password")
STAGE_AUDIENCE = os.getenv("stage_audience", default=None)
PROD_AUDIENCE = os.getenv("prod_audience", default=None)

if ENVIRONMENT == "local":
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.expanduser("~/keys/jsm-trigger-account.json")
