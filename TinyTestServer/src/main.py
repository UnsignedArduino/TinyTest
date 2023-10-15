import logging

import uvicorn
from fastapi import FastAPI

from routers import users
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

app = FastAPI()
app.include_router(users.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=4000)
