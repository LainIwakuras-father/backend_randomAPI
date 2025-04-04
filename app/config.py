import logging
import os
import sys

from dotenv import load_dotenv

load_dotenv()
VK_TOKEN = os.getenv("VK_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL")


from pydantic import BaseModel

LOG_DEFAULT_FORMAT = (
    "[%(asctime)s.%(msecs)03d] %(module)10s:%(lineno)-3d %(levelname)-7s - %(message)s"
)


class LoggerConfig(BaseModel):
    level: int = logging.DEBUG
    format: str = LOG_DEFAULT_FORMAT


loggerConfig = LoggerConfig()
