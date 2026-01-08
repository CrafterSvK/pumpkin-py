from __future__ import annotations

from typing import Any

from sqlalchemy import BigInteger, UniqueConstraint
from sqlalchemy.orm import mapped_column, Mapped

from pie.database import session, Base


class SpamChannel(Base):
    __tablename__ = "spamchannels"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int] = mapped_column(BigInteger)
    primary: Mapped[bool] = mapped_column(default=False)

    __table_args__ = (
        UniqueConstraint(guild_id, channel_id),
        UniqueConstraint(channel_id, primary),
    )

    @staticmethod
    def add(guild_id: int, channel_id: int) -> SpamChannel:
        channel = SpamChannel(guild_id=guild_id, channel_id=channel_id)
        session.add(channel)
        session.commit()
        return channel

    @staticmethod
    def get(guild_id: int, channel_id: int) -> SpamChannel | None:
        query = (
            session.query(SpamChannel)
            .filter_by(guild_id=guild_id, channel_id=channel_id)
            .one_or_none()
        )
        return query

    @staticmethod
    def get_all(guild_id: int) -> list[SpamChannel]:
        query = session.query(SpamChannel).filter_by(guild_id=guild_id).all()
        return query

    @staticmethod
    def set_primary(guild_id: int, channel_id: int) -> SpamChannel | None:
        query = (
            session.query(SpamChannel)
            .filter_by(guild_id=guild_id, primary=True)
            .one_or_none()
        )
        if query and query.channel_id == channel_id:
            return query
        if query:
            query.primary = False

        query = SpamChannel.get(guild_id, channel_id)
        if query:
            query.primary = True

        session.commit()
        return query

    @staticmethod
    def remove(guild_id: int, channel_id):
        query = (
            session.query(SpamChannel)
            .filter_by(guild_id=guild_id, channel_id=channel_id)
            .delete()
        )
        session.commit()
        return query

    def __repr__(self) -> str:
        return (
            f'<{self.__class__.__name__} idx="{self.idx}" '
            f'guild_id="{self.guild_id}" channel_id="{self.channel_id}" '
            f'primary="{self.primary}">'
        )

    def dump(self) -> dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "primary": self.primary,
        }
