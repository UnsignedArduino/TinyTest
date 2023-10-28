import logging
from typing import Optional

from sqlalchemy import select, text
from sqlalchemy.orm import Session

from database.connection import engine
from database.schema.sprts import AddSPRT, DBSPRT
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


def sprt_id_exists(sprt_id: int) -> bool:
    with engine.connect() as conn:
        return (
            conn.execute(
                text("SELECT COUNT(id) FROM sprts WHERE id=:id"),
                {"id": sprt_id},
            ).first()[0]
            > 0
        )


def id_get_sprt(sprt_id: int) -> Optional[DBSPRT]:
    with Session(engine) as session:
        sprts = session.execute(select(DBSPRT).where(DBSPRT.id == sprt_id)).all()
        if len(sprts) > 0:
            return sprts[0][0]


def get_all_sprts(limit: int = 100, offset: int = 0) -> list[DBSPRT]:
    with Session(engine) as session:
        return list(session.scalars(select(DBSPRT).limit(limit).offset(offset)).all())


def get_sprt_count() -> int:
    with Session(engine) as session:
        return session.execute(text("SELECT COUNT(id) FROM sprts")).first()[0]


def add_sprt(add_sprt: AddSPRT) -> int:
    logger.debug(f"Adding SPRT {add_sprt}")
    with Session(engine) as session:
        db_sprt = DBSPRT(**add_sprt.model_dump(), games_queued=add_sprt.max_games)
        if add_sprt.paused:
            db_sprt.result = "Paused"
        session.add(db_sprt)
        session.commit()
        return db_sprt.id


def id_delete_sprt(sprt_id: int):
    logger.debug(f"Deleting SPRT with ID {sprt_id}")
    with Session(engine) as session:
        sprt = id_get_sprt(sprt_id)
        if sprt is not None:
            session.delete(sprt)
            session.commit()
        else:
            logger.debug(f"Could not find SPRT with ID {sprt_id} to delete")
