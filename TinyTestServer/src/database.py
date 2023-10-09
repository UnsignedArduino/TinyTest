from sqlalchemy import create_engine

from consts import DATABASE_URL

engine = create_engine(DATABASE_URL)
