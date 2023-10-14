import asyncio as aio
import logging
from secrets import compare_digest

import ngrok
from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from consts import DATABASE_URL_API_KEY, NGROK_KEY
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

router = APIRouter()

ngrok_client = ngrok.Client(NGROK_KEY)

database_url = None


class APIKey(BaseModel):
    key: str


@router.post("/database_url", response_class=PlainTextResponse)
async def post_database_url(apiKey: APIKey):
    if compare_digest(apiKey.key, DATABASE_URL_API_KEY):
        return database_url
    else:
        raise HTTPException(status_code=401, detail="Unauthorized to get database URL")


async def check_database_url():
    global database_url
    logger.debug("Starting database URL check task")
    while True:
        logger.debug("Checking for database URL")
        all_tunnels = ngrok_client.tunnels.list().tunnels
        if len(all_tunnels) == 0:
            logger.warning("Database tunnel not found, database down?")
            database_url = None
        elif len(all_tunnels) > 1:
            logger.warning("Too many database tunnels, ambiguous!")
            database_url = None
        else:
            database_url = all_tunnels[0].public_url.replace("tcp://", "")
            logger.debug("Found public URL")
        await aio.sleep(60)
