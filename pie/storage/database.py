from __future__ import annotations

from typing import Any, cast

from sqlalchemy import BigInteger, CursorResult, delete
from sqlalchemy.orm import mapped_column, Mapped

from pie.database import session, Base


class StorageData(Base):
    __tablename__ = "pie_storage_data"

    module: Mapped[str] = mapped_column(primary_key=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    key: Mapped[str] = mapped_column(primary_key=True)
    value: Mapped[str] = mapped_column()
    type: Mapped[str] = mapped_column()

    @staticmethod
    def set(
        module: str,
        guild_id: int,
        key: str,
        value,
        allow_overwrite: bool = True,
    ) -> StorageData | None:
        data = (
            session.query(StorageData)
            .filter_by(module=module)
            .filter_by(guild_id=guild_id)
            .filter_by(key=key)
            .one_or_none()
        )

        if data and not allow_overwrite:
            return None

        if not data:
            data = StorageData(module=module, key=key, guild_id=guild_id)

        data.value = value
        data.type = type(value).__name__
        session.merge(data)
        session.commit()

        return data

    @staticmethod
    def get(module: str, guild_id: int, key: str) -> StorageData | None:
        data = (
            session.query(StorageData)
            .filter_by(module=module)
            .filter_by(guild_id=guild_id)
            .filter_by(key=key)
            .one_or_none()
        )
        return data

    @staticmethod
    def remove(module: str, guild_id: int, key: str) -> bool:
        result = session.execute(
            delete(StorageData)
            .where(StorageData.module == module)
            .where(StorageData.guild_id == guild_id)
            .where(StorageData.key == key)
        )
        session.commit()

        return cast(CursorResult, result).rowcount == 1

    def __repr__(self) -> str:
        return (
            f'<StorageData module="{self.module}" guild_id="{self.guild_id}" key="{self.key}" '
            f'value="{self.value}" type="{self.type}">'
        )

    def dump(self) -> dict[str, Any]:
        """Return object representation as dictionary for easy serialisation."""
        return {
            "module": self.module,
            "guild_id": self.guild_id,
            "key": self.key,
            "value": self.value,
        }
