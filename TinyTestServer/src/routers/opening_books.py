import logging
from base64 import b85decode, b85encode
from typing import Annotated

from fastapi import APIRouter, Body, HTTPException, Header, Response, UploadFile, status

from database.crud.opening_books import (
    book_id_exist,
    id_delete_book,
    id_get_all_books,
    id_get_book,
    id_get_book_contents,
    id_set_book,
    id_set_book_contents,
)
from database.crud.users import is_api_key_admin
from database.schema.opening_books import OpeningBookWithoutContents
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

router = APIRouter(
    prefix="/opening-books",
    tags=["opening books"],
)

StringHeader = Annotated[str | None, Header()]


@router.get("", summary="Get book info from ID.")
async def get_root(book_id: int):
    if not book_id_exist(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return id_get_book(book_id)


@router.get("/all", summary="Get all books.")
async def get_root():
    return id_get_all_books()


@router.get("/content", summary="Get book content from ID.")
async def get_content(book_id: int):
    if not book_id_exist(book_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    meta = id_get_book(book_id)
    contents = b85decode(id_get_book_contents(book_id))

    filename = (
        meta.name.replace(" ", "_") + "." + meta.book_format + ".zip"
        if meta.compression_format == "zip"
        else ""
    )

    if meta.compression_format == "zip":
        media_type = "application/zip"
    else:
        if meta.book_format == "pgn":
            media_type = "application/vnd.chess-pgn"
        else:
            media_type = "text/plain"

    headers = {"Content-Disposition": f'attachment; filename="{filename}"'}
    return Response(contents, headers=headers, media_type=media_type)


@router.post(
    "",
    summary="Set book info.",
)
async def post_root(
    opening_book: Annotated[OpeningBookWithoutContents, Body()],
    x_api_token: StringHeader = None,
) -> int:
    if not is_api_key_admin(x_api_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return id_set_book(opening_book)


@router.post(
    "/content",
    summary="Set book content.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def post_content(
    book_id: int,
    file: UploadFile,
    x_api_token: StringHeader = None,
) -> None:
    if not is_api_key_admin(x_api_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    id_set_book_contents(
        book_id, b85encode(await file.read()).decode() if file else None
    )


@router.delete(
    "",
    summary="Delete book.",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_root(
    book_id: int,
    x_api_token: StringHeader = None,
) -> None:
    if not is_api_key_admin(x_api_token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    id_delete_book(book_id)
