import logging
from math import ceil
from typing import Annotated

from fastapi import APIRouter, HTTPException, Header, status

from database.crud.sprts import (
    get_all_sprts,
    get_sprt_count,
    id_get_sprt,
    sprt_id_exists,
)
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

router = APIRouter(
    prefix="/sprts",
    tags=["sprts"],
)

StringHeader = Annotated[str | None, Header()]


@router.get("", summary="Get SPRT from ID.")
async def get_root(sprt_id: int):
    if not sprt_id_exists(sprt_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return id_get_sprt(sprt_id)


PAGE_SIZE = 100


@router.get("/page", summary="Get SPRTs by page.")
async def get_page(page: int = 0):
    if page < 0 or page > (await get_page_count() - 1):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return get_all_sprts(PAGE_SIZE, page * PAGE_SIZE)


@router.get("/page/count", summary="Get page count of SPRTs.")
async def get_page_count():
    return ceil(get_sprt_count() / PAGE_SIZE)
