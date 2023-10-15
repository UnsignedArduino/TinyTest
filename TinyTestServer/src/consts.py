import logging
import os

from dotenv import load_dotenv

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

logger.debug("Loading dotenv")
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")

API_KEY_LENGTH = 32
