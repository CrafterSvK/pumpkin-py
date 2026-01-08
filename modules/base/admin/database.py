from __future__ import annotations

from typing import cast

from sqlalchemy import select
from sqlalchemy.orm import Mapped, mapped_column

from pie.database import session, Base


class BaseAdminModule(Base):
    __tablename__ = "base_admin_modules"

    name: Mapped[str] = mapped_column(primary_key=True)
    enabled: Mapped[bool] = mapped_column(default=True)

    @staticmethod
    def add(name: str, enabled: bool) -> BaseAdminModule:
        """Add new module entry to database."""
        module = BaseAdminModule(name=name, enabled=enabled)
        session.merge(module)
        session.commit()
        return module

    @staticmethod
    def get(name: str) -> BaseAdminModule | None:
        """Get module entry."""
        return session.execute(
            select(BaseAdminModule).where(BaseAdminModule.name == name)
        ).scalar_one_or_none()

    @staticmethod
    def get_all() -> list[BaseAdminModule]:
        """Get all modules."""
        modules = session.execute(select(BaseAdminModule)).scalars().all()

        return cast(list[BaseAdminModule], modules)

    def __repr__(self) -> str:
        return f'<BaseAdminModule name="{self.name}" enabled="{self.enabled}">'
