from __future__ import annotations

from sqlalchemy.orm import mapped_column, Mapped

from pie.database import session, Base


class Config(Base):
    """Global bot configuration."""

    __tablename__ = "config"

    idx: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    prefix: Mapped[str] = mapped_column(default="!")
    language: Mapped[str] = mapped_column(default="en")
    status: Mapped[str] = mapped_column(default="online")

    @staticmethod
    def get() -> Config:
        """Get instance of global bot settings.

        If there is none, it will be created with the default values.

        .. list-table:: Default values for configuration
           :widths: 25 25 25
           :header-rows: 1

           * - Attribute
             - Type
             - Default value
           * - prefix
             - :class:`str`
             - ``!``
           * - language
             - :class:`str`
             - ``en``
           * - status
             - :class:`str`
             - ``online``
        """
        query = session.query(Config).one_or_none()
        if query is None:
            query = Config()
            session.add(query)
            session.commit()
        return query

    def save(self) -> None:
        """Save global settings."""
        session.merge(self)
        session.commit()

    def __repr__(self) -> str:
        return (
            f'<Config status="{self.status}" '
            f'prefix="{self.prefix}" language="{self.language}">'
        )

    def dump(self) -> dict[str, bool | str]:
        return {
            "prefix": self.prefix,
            "language": self.language,
            "status": self.status,
        }
