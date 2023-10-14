import asyncio as aio
import logging

import uvicorn
from fastapi import FastAPI

from routers import database_url
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

app = FastAPI()
app.include_router(database_url.router)


@app.on_event("startup")
async def on_startup():
    logger.debug("Starting startup tasks")
    aio.create_task(database_url.check_database_url())


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=80)
