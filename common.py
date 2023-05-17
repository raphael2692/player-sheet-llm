

import json
import os
from loguru import logger as LOGGER


def set_env():
    with open("secrets.json", "r") as jsonfile:
        secrets = json.load(jsonfile)
    os.environ["OPENAI_API_KEY"] = secrets["openai_key"]