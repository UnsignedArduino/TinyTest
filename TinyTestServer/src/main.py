import logging

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from consts import PORT
from routers import opening_books, sprts, users
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)

app = FastAPI()
app.include_router(users.router)
app.include_router(opening_books.router)
app.include_router(sprts.router)

origins = [
    "http://localhost:3000",
    "https://tinytest-beta.vercel.app",
    "https://tinytest.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex="https:\/\/tinytest-.*\-unsignedarduino\.vercel\.app",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    logger.debug("Starting WSGI server")
    uvicorn.run("main:app", host="0.0.0.0", port=PORT)
