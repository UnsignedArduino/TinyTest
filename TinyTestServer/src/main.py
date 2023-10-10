import logging

import uvicorn
from fastapi import FastAPI

from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

app = FastAPI()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80)
