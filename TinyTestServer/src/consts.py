import logging
import os

from dotenv import load_dotenv

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

logger.debug("Loading dotenv")
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
