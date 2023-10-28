import logging
from math import ceil
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Header, status

from database.crud.sprts import (
    add_sprt,
    get_all_sprts,
    get_sprt_count,
    id_delete_sprt,
    id_get_sprt,
    sprt_id_exists,
)
from database.crud.users import is_api_key_admin
from database.schema.sprts import AddSPRT
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
async def get_page_count() -> int:
    return ceil(get_sprt_count() / PAGE_SIZE)


@router.post(
    "",
    summary="Add SPRT.",
)
async def post_root(
    sprt: Annotated[AddSPRT, Body()],
    x_api_token: StringHeader = None,
) -> int:
    if not is_api_key_admin(x_api_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return add_sprt(sprt)


@router.delete(
    "",
    summary="Delete SPRT.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_root(
    sprt_id: int,
    x_api_token: StringHeader = None,
) -> None:
    if not is_api_key_admin(x_api_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    id_delete_sprt(sprt_id)
