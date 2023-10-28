from typing import Optional

from pydantic import BaseModel
from sqlalchemy import ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from database.schema.base import DBBase


class SPRT(BaseModel):
    id: int
    engine_1_git_url: str
    engine_1_commit: str
    engine_2_git_url: str
    engine_2_commit: str
    elo0: int
    elo1: int
    alpha: float
    beta: float
    max_games: int
    game_pgns_to_save: int = 0
    time_control: str
    opening_book_id: Optional[int]
    games_queued: int
    games_running: int = 0
    games_finished_white_mate: int = 0
    games_finished_black_mate: int = 0
    games_finished_draw: int = 0
    games_finished_canceled: int = 0
    games_finished_error: int = 0
    result: str
    scheduled_by: int
    queue_time: int
    start_time: Optional[int]
    end_time: Optional[int]
    priority: int = 0
    paused: bool = False


class AddSPRT(BaseModel):
    engine_1_git_url: str
    engine_1_commit: str
    engine_2_git_url: str
    engine_2_commit: str
    elo0: int
    elo1: int
    alpha: float
    beta: float
    max_games: int
    game_pgns_to_save: int = 0
    time_control: str
    opening_book_id: Optional[int]
    scheduled_by: int
    priority: int = 0
    paused: bool = False


class DBSPRT(DBBase):
    __tablename__ = "sprts"

    id: Mapped[int] = mapped_column(primary_key=True)
    engine_1_git_url: Mapped[str] = mapped_column(String(255))
    engine_1_commit: Mapped[str] = mapped_column(String(40))
    engine_2_git_url: Mapped[str] = mapped_column(String(255))
    engine_2_commit: Mapped[str] = mapped_column(String(40))
    elo0: Mapped[int]
    elo1: Mapped[int]
    alpha: Mapped[float]
    beta: Mapped[float]
    max_games: Mapped[int]
    game_pgns_to_save: Mapped[int] = 0
    time_control: Mapped[str] = mapped_column(String(16))
    opening_book_id = mapped_column(ForeignKey("opening_books.id"))
    games_queued: Mapped[int]
    games_running: Mapped[int] = 0
    games_finished_white_mate: Mapped[int] = 0
    games_finished_black_mate: Mapped[int] = 0
    games_finished_draw: Mapped[int] = 0
    games_finished_canceled: Mapped[int] = 0
    games_finished_error: Mapped[int] = 0
    result: Mapped[str] = mapped_column(Text, server_default="Waiting for approval")
    scheduled_by = mapped_column(ForeignKey("users.id"))
    queue_time: Mapped[int] = mapped_column(
        Integer, server_default=func.current_timestamp()
    )
    start_time: Mapped[int]
    end_time: Mapped[int]
    priority: Mapped[int] = 0
    paused: Mapped[bool]

    def __repr__(self) -> str:
        return (
            f"DBSPRT("
            f"id={self.id!r}, "
            f"engine_1_git_url={self.engine_1_git_url!r}, "
            f"engine_1_commit={self.engine_1_commit!r}, "
            f"engine_2_git_url={self.engine_2_git_url!r}, "
            f"engine_2_commit={self.engine_2_commit!r}, "
            f"elo0={self.elo0!r}, "
            f"elo1={self.elo1!r}, "
            f"alpha={self.alpha!r}, "
            f"beta={self.beta!r}, "
            f"max_games={self.max_games!r}, "
            f"game_pgns_to_save={self.game_pgns_to_save!r}, "
            f"time_control={self.time_control!r}, "
            f"opening_book_id={self.opening_book_id!r}, "
            f"games_queued={self.games_queued!r}, "
            f"games_running={self.games_running!r}, "
            f"games_finished_white_mate={self.games_finished_white_mate!r}, "
            f"games_finished_black_mate={self.games_finished_black_mate!r}, "
            f"games_finished_draw={self.games_finished_draw!r}, "
            f"games_finished_canceled={self.games_finished_canceled!r}, "
            f"games_finished_error={self.games_finished_error!r}, "
            f"result={self.result!r}, "
            f"scheduled_by={self.scheduled_by!r}, "
            f"queue_time={self.queue_time!r}, "
            f"start_time={self.start_time!r}, "
            f"end_time={self.end_time!r}, "
            f"priority={self.priority!r}, "
            f"paused={self.paused!r}"
            f")"
        )
