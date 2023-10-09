import logging

from sqlalchemy import create_engine

from consts import DATABASE_URL
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

engine = create_engine(DATABASE_URL)
