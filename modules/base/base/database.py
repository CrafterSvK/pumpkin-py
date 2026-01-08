from __future__ import annotations

from typing import cast

from sqlalchemy import BigInteger, select, delete, CursorResult
from sqlalchemy.orm import Mapped, mapped_column

from pie.database import session, Base


class UserPin(Base):
    __tablename__ = "base_base_userpin"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int | None] = mapped_column(BigInteger, default=None)
    limit: Mapped[int] = mapped_column(default=0)

    @staticmethod
    def add(guild_id: int, channel_id: int | None, limit: int = 0) -> UserPin:
        """Add userpin preference."""
        if UserPin.get(guild_id, channel_id) is not None:
            UserPin.remove(guild_id, channel_id)
        query = UserPin(guild_id=guild_id, channel_id=channel_id, limit=limit)
        session.add(query)
        session.commit()
        return query

    @staticmethod
    def get(guild_id: int, channel_id: int | None) -> UserPin | None:
        """Get userpin preferences for the guild."""
        user_pin = session.execute(
            select(UserPin)
            .where(UserPin.guild_id == guild_id)
            .where(UserPin.channel_id == channel_id)
        ).scalar_one_or_none()
        return user_pin

    @staticmethod
    def get_all(guild_id: int) -> list[UserPin]:
        user_pins = (
            session.execute(select(UserPin).where(UserPin.guild_id == guild_id))
            .scalars()
            .all()
        )

        return cast(list[UserPin], user_pins)

    @staticmethod
    def remove(guild_id: int, channel_id: int | None) -> int:
        result = session.execute(
            delete(UserPin)
            .where(UserPin.guild_id == guild_id)
            .where(UserPin.channel_id == channel_id)
        )
        session.commit()
        return cast(CursorResult, result).rowcount

    def __repr__(self) -> str:
        return (
            f"<UserPin idx='{self.idx}' guild_id='{self.guild_id}' "
            f"channel_id='{self.channel_id}' limit='{self.limit}'>"
        )

    def dump(self) -> dict:
        return {
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "limit": self.limit,
        }


class UserThread(Base):
    __tablename__ = "base_base_userthread"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int | None] = mapped_column(BigInteger, default=None)
    limit: Mapped[int] = mapped_column(default=0)

    @staticmethod
    def add(guild_id: int, channel_id: int | None, limit: int = 0) -> UserThread:
        """Add userthread preference."""
        if UserThread.get(guild_id, channel_id) is not None:
            UserThread.remove(guild_id, channel_id)
        user_thread = UserThread(guild_id=guild_id, channel_id=channel_id, limit=limit)
        session.add(user_thread)
        session.commit()
        return user_thread

    @staticmethod
    def get(guild_id: int, channel_id: int | None) -> UserThread | None:
        """Get userthread preference for the guild."""
        result = session.execute(
            select(UserThread)
            .where(UserThread.guild_id == guild_id)
            .where(UserThread.channel_id == channel_id)
        ).scalar_one_or_none()
        return result

    @staticmethod
    def get_all(guild_id: int) -> list[UserThread]:
        user_threads = (
            session.execute(select(UserThread).where(UserThread.guild_id == guild_id))
            .scalars()
            .all()
        )
        return cast(list[UserThread], user_threads)

    @staticmethod
    def remove(guild_id: int, channel_id: int | None) -> int:
        result = session.execute(
            delete(UserThread)
            .where(UserThread.guild_id == guild_id)
            .where(UserThread.channel_id == channel_id)
        )
        session.commit()
        return cast(CursorResult, result).rowcount

    def __repr__(self) -> str:
        return (
            f"<UserThread idx='{self.idx}' guild_id='{self.guild_id}' "
            f"channel_id='{self.channel_id}' limit='{self.limit}'>"
        )

    def dump(self) -> dict:
        return {
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "limit": self.limit,
        }


class Bookmark(Base):
    __tablename__ = "base_base_bookmarks"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int | None] = mapped_column(BigInteger, default=None)
    enabled: Mapped[bool] = mapped_column(default=False)

    @staticmethod
    def add(guild_id: int, channel_id: int | None, enabled: bool = False) -> Bookmark:
        if Bookmark.get(guild_id, channel_id) is not None:
            Bookmark.remove(guild_id, channel_id)
        query = Bookmark(guild_id=guild_id, channel_id=channel_id, enabled=enabled)
        session.add(query)
        session.commit()
        return query

    @staticmethod
    def get(guild_id: int, channel_id: int | None) -> Bookmark | None:
        result = session.execute(
            select(Bookmark)
            .where(Bookmark.guild_id == guild_id)
            .where(Bookmark.channel_id == channel_id)
        ).scalar_one_or_none()
        return result

    @staticmethod
    def get_all(guild_id: int) -> list[Bookmark]:
        result = (
            session.execute(select(Bookmark).where(Bookmark.guild_id == guild_id))
            .scalars()
            .all()
        )
        return cast(list[Bookmark], result)

    @staticmethod
    def remove(guild_id: int, channel_id: int | None) -> int:
        result = session.execute(
            delete(Bookmark)
            .where(Bookmark.guild_id == guild_id)
            .where(Bookmark.channel_id == channel_id)
        )
        session.commit()
        return cast(CursorResult, result).rowcount

    def __repr__(self) -> str:
        return (
            f"<Bookmark idx='{self.idx}' guild_id='{self.guild_id}' "
            f"channel_id='{self.channel_id}' enabled='{self.enabled}'>"
        )

    def dump(self) -> dict:
        return {
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "enabled": self.enabled,
        }


class AutoThread(Base):
    __tablename__ = "base_base_autothread"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int] = mapped_column(BigInteger)
    duration: Mapped[int] = mapped_column()

    @staticmethod
    def add(guild_id: int, channel_id: int, duration: int) -> AutoThread:
        query = AutoThread.get(guild_id, channel_id)
        if query:
            query.duration = duration
        else:
            query = AutoThread(
                guild_id=guild_id, channel_id=channel_id, duration=duration
            )
        session.add(query)
        session.commit()
        return query

    @staticmethod
    def get(guild_id: int, channel_id: int) -> AutoThread | None:
        result = session.execute(
            select(AutoThread)
            .where(AutoThread.guild_id == guild_id)
            .where(AutoThread.channel_id == channel_id)
        ).scalar_one_or_none()
        return result

    @staticmethod
    def get_all(guild_id: int) -> list[AutoThread]:
        result = (
            session.execute(select(AutoThread).where(AutoThread.guild_id == guild_id))
            .scalars()
            .all()
        )
        return cast(list[AutoThread], result)

    @staticmethod
    def remove(guild_id: int, channel_id: int) -> int:
        result = session.execute(
            delete(AutoThread)
            .where(AutoThread.guild_id == guild_id)
            .where(AutoThread.channel_id == channel_id)
        )
        session.commit()
        return cast(CursorResult, result).rowcount

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"guild_id='{self.guild_id} channel_id='{self.channel_id} duration='{self.duration}'>"
        )
