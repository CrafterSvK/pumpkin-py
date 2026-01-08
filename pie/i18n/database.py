from __future__ import annotations

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column

from pie.database import session, Base


class GuildLanguage(Base):
    """Language preference for the guild.

    .. note::
        See text translation at :class:`core.i18n.Translator`.

        See command API at :class:`modules.base.language.module`.
    """

    __tablename__ = "language_guilds"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger, unique=True)
    language: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return (
            f'<GuildLanguage idx="{self.idx}" '
            f'guild_id="{self.guild_id}" language="{self.language}">'
        )

    def __eq__(self, obj) -> bool:
        return type(self) is type(obj) and self.guild_id == obj.guild_id

    def dump(self) -> dict[str, int | str]:
        return {
            "guild_id": self.guild_id,
            "language": self.language,
        }

    @staticmethod
    def add(guild_id: int, language: str) -> GuildLanguage:
        """Add guild language preference.

        :param guild_id: Guild ID.
        :param language: One of the supported languages. Please note that this
            parameter is not checked on database level and it's your
            responsibility to make sure it has correct value.
        :return: Created guild language preference.
        """
        preference = GuildLanguage(guild_id=guild_id, language=language)

        # remove old language preference
        session.query(GuildLanguage).filter_by(guild_id=guild_id).delete()

        session.add(preference)
        session.commit()
        return preference

    @staticmethod
    def get(guild_id: int) -> GuildLanguage | None:
        """Get guild language preference.

        :param guild_id: Guild ID.
        :return: Guild language preference or ``None``.
        """
        query = session.query(GuildLanguage).filter_by(guild_id=guild_id).one_or_none()
        return query

    @staticmethod
    def remove(guild_id: int) -> int:
        """Remove guild language preference.

        :param guild_ID: Guild ID.
        :return: Number of deleted preferences, always ``0`` or ``1``.
        """
        query = session.query(GuildLanguage).filter_by(guild_id=guild_id).delete()
        session.commit()
        return query


class MemberLanguage(Base):
    """Language preference of the user.

    .. note::
        See text translation at :class:`core.text.Translator`.

        See command API at :class:`modules.base.language.module`.
    """

    __tablename__ = "language_members"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    guild_id: Mapped[int] = mapped_column(BigInteger)
    member_id: Mapped[int] = mapped_column(BigInteger)
    language: Mapped[str] = mapped_column()

    def __repr__(self) -> str:
        return (
            f'<MemberLanguage idx="{self.idx}" guild_id="{self.guild_id}" '
            f'member_id="{self.member_id}" language="{self.language}">'
        )

    def __eq__(self, obj) -> bool:
        return (
            type(self) is type(obj)
            and self.guild_id == obj.guild_id
            and self.member_id == obj.member_id
        )

    def dump(self) -> dict[str, int | str]:
        return {
            "guild_id": self.guild_id,
            "member_id": self.member_id,
            "language": self.language,
        }

    @staticmethod
    def add(guild_id: int, member_id: int, language: str) -> MemberLanguage:
        """Add member language preference.

        :param guild_id: Guild ID.
        :param member_id: Member ID.
        :param language: One of the supported languages. Please note that this
            parameter is not checked on database level and it's your
            responsibility to make sure it has correct value.
        :return: Created member language preference.
        """
        preference = MemberLanguage.get(guild_id, member_id)
        if preference:
            preference.language = language
        else:
            preference = MemberLanguage(
                guild_id=guild_id, member_id=member_id, language=language
            )
            session.add(preference)

        session.commit()
        return preference

    @staticmethod
    def get(guild_id: int, member_id: int) -> MemberLanguage | None:
        """Get member language preference.

        :param guild_id: Guild ID.
        :param member_id: Member ID.
        :return: Member language preference or ``None``.
        """
        query = (
            session.query(MemberLanguage)
            .filter_by(guild_id=guild_id, member_id=member_id)
            .one_or_none()
        )
        return query

    @staticmethod
    def remove(guild_id: int, member_id: int) -> int:
        """Remove member language preference.

        :param guild_ID: Guild ID.
        :param member_id: Member ID.
        :return: Number of deleted preferences, always ``0`` or ``1``.
        """
        query = (
            session.query(MemberLanguage)
            .filter_by(guild_id=guild_id, member_id=member_id)
            .delete()
        )
        session.commit()
        return query
