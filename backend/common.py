

import json
import os
from datetime import datetime
from loguru import logger as LOGGER

LOGGER.add(f"logs/file_{datetime.now()}.log", rotation="10 MB")

def set_env():
    with open("secrets.json", "r") as jsonfile:
        secrets = json.load(jsonfile)
    os.environ["OPENAI_API_KEY"] = secrets["openai_key"]