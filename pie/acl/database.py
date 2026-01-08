from __future__ import annotations

import enum
from typing import Any

from sqlalchemy import BigInteger, Boolean, Column, Enum
from sqlalchemy.orm import Mapped, mapped_column

from pie.database import session, Base


class ACLevel(enum.IntEnum):
    BOT_OWNER = 5
    GUILD_OWNER = 4
    MOD = 3
    SUBMOD = 2
    MEMBER = 1
    EVERYONE = 0


class ACDefault(Base):
    __tablename__ = "pie_acl_acdefault"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    command: Mapped[str] = mapped_column()
    level: Mapped[ACLevel] = mapped_column(Enum(ACLevel))

    @staticmethod
    def add(guild_id: int, command: str, level: ACLevel) -> ACDefault | None:
        if ACDefault.get(guild_id, command):
            return None

        default = ACDefault(guild_id=guild_id, command=command, level=level)
        session.add(default)
        session.commit()
        return default

    @staticmethod
    def get(guild_id: int, command: str) -> ACDefault | None:
        default = (
            session.query(ACDefault)
            .filter_by(guild_id=guild_id, command=command)
            .one_or_none()
        )
        return default

    @staticmethod
    def get_all(guild_id: int) -> list[ACDefault]:
        query = session.query(ACDefault).filter_by(guild_id=guild_id).all()
        return query

    @staticmethod
    def remove(guild_id: int, command: str) -> bool:
        query = (
            session.query(ACDefault)
            .filter_by(guild_id=guild_id, command=command)
            .delete()
        )
        return query > 0

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            + " ".join(f"{key}='{value}'" for key, value in self.dump().items())
            + ">"
        )

    def dump(self) -> dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "command": self.command,
            "level": self.level.name,
        }


class RoleOverwrite(Base):
    __tablename__ = "pie_acl_role_overwrite"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    role_id: Mapped[int] = mapped_column(BigInteger)
    command: Mapped[str] = mapped_column()
    allow = Column(Boolean)

    @staticmethod
    def add(
        guild_id: int, role_id: int, command: str, allow: bool
    ) -> RoleOverwrite | None:
        if RoleOverwrite.get(guild_id, role_id, command):
            return None
        ro = RoleOverwrite(
            guild_id=guild_id, role_id=role_id, command=command, allow=allow
        )
        session.add(ro)
        session.commit()
        return ro

    @staticmethod
    def get(guild_id: int, role_id: int, command: str) -> RoleOverwrite | None:
        ro = (
            session.query(RoleOverwrite)
            .filter_by(guild_id=guild_id, role_id=role_id, command=command)
            .one_or_none()
        )
        return ro

    @staticmethod
    def get_all(guild_id: int) -> list[RoleOverwrite]:
        query = session.query(RoleOverwrite).filter_by(guild_id=guild_id).all()
        return query

    @staticmethod
    def remove(guild_id: int, role_id: int, command: str) -> bool:
        query = (
            session.query(RoleOverwrite)
            .filter_by(guild_id=guild_id, role_id=role_id, command=command)
            .delete()
        )
        return query > 0

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            + " ".join(f"{key}='{value}'" for key, value in self.dump().items())
            + ">"
        )

    def dump(self) -> dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "role_id": self.role_id,
            "allow": self.allow,
        }


class UserOverwrite(Base):
    __tablename__ = "pie_acl_user_overwrite"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    user_id: Mapped[int] = mapped_column(BigInteger)
    command: Mapped[str] = mapped_column()
    allow = Column(Boolean)

    @staticmethod
    def add(
        guild_id: int, user_id: int, command: str, allow: bool
    ) -> UserOverwrite | None:
        if UserOverwrite.get(guild_id, user_id, command):
            return None
        uo = UserOverwrite(
            guild_id=guild_id, user_id=user_id, command=command, allow=allow
        )
        session.add(uo)
        session.commit()
        return uo

    @staticmethod
    def get(guild_id: int, user_id: int, command: str) -> UserOverwrite | None:
        uo = (
            session.query(UserOverwrite)
            .filter_by(guild_id=guild_id, user_id=user_id, command=command)
            .one_or_none()
        )
        return uo

    @staticmethod
    def get_all(guild_id: int) -> list[UserOverwrite]:
        query = session.query(UserOverwrite).filter_by(guild_id=guild_id).all()
        return query

    @staticmethod
    def remove(guild_id: int, user_id: int, command: str) -> bool:
        query = (
            session.query(UserOverwrite)
            .filter_by(guild_id=guild_id, user_id=user_id, command=command)
            .delete()
        )
        return query > 0

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            + " ".join(f"{key}='{value}'" for key, value in self.dump().items())
            + ">"
        )

    def dump(self) -> dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "user_id": self.user_id,
            "allow": self.allow,
        }


class ChannelOverwrite(Base):
    __tablename__ = "pie_acl_channel_overwrite"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    channel_id: Mapped[int] = mapped_column(BigInteger)
    command: Mapped[str] = mapped_column()
    allow = Column(Boolean)

    @staticmethod
    def add(
        guild_id: int, channel_id: int, command: str, allow: bool
    ) -> ChannelOverwrite | None:
        if ChannelOverwrite.get(guild_id, channel_id, command):
            return None
        co = ChannelOverwrite(
            guild_id=guild_id, channel_id=channel_id, command=command, allow=allow
        )
        session.add(co)
        session.commit()
        return co

    @staticmethod
    def get(guild_id: int, channel_id: int, command: str) -> ChannelOverwrite | None:
        co = (
            session.query(ChannelOverwrite)
            .filter_by(guild_id=guild_id, channel_id=channel_id, command=command)
            .one_or_none()
        )
        return co

    @staticmethod
    def get_all(guild_id: int) -> list[ChannelOverwrite]:
        query = session.query(ChannelOverwrite).filter_by(guild_id=guild_id).all()
        return query

    @staticmethod
    def remove(guild_id: int, channel_id: int, command: str) -> bool:
        query = (
            session.query(ChannelOverwrite)
            .filter_by(guild_id=guild_id, channel_id=channel_id, command=command)
            .delete()
        )
        return query > 0

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            + " ".join(f"{key}='{value}'" for key, value in self.dump().items())
            + ">"
        )

    def dump(self) -> dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "channel_id": self.channel_id,
            "allow": self.allow,
        }


class ACLevelMappping(Base):
    __tablename__ = "pie_acl_aclevel_mapping"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    role_id: Mapped[int] = mapped_column(BigInteger)
    level: Mapped[ACLevel] = mapped_column(Enum(ACLevel))

    @staticmethod
    def add(guild_id: int, role_id: int, level: ACLevel) -> ACLevelMappping | None:
        if ACLevelMappping.get(guild_id, role_id):
            return None
        m = ACLevelMappping(guild_id=guild_id, role_id=role_id, level=level)
        session.add(m)
        session.commit()
        return m

    @staticmethod
    def get(guild_id: int, role_id: int) -> ACLevelMappping | None:
        m = (
            session.query(ACLevelMappping)
            .filter_by(guild_id=guild_id, role_id=role_id)
            .one_or_none()
        )
        return m

    @staticmethod
    def get_all(guild_id: int) -> list[ACLevelMappping]:
        m = session.query(ACLevelMappping).filter_by(guild_id=guild_id).all()
        return m

    @staticmethod
    def remove(guild_id: int, role_id: int) -> bool:
        query = (
            session.query(ACLevelMappping)
            .filter_by(guild_id=guild_id, role_id=role_id)
            .delete()
        )
        return query > 0

    def __repr__(self) -> str:
        return (
            f"<{self.__class__.__name__} "
            f"guild_id='{self.guild_id}' role_id='{self.role_id}' "
            f"level='{self.level.name}'>"
        )

    def dump(self) -> dict[str, Any]:
        return {
            "guild_id": self.guild_id,
            "role_id": self.role_id,
            "level": self.level,
        }
