from sqlalchemy.orm import Mapped, mapped_column

from . import Base


class Form(Base):
    __tablename__ = "forms"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    uuid: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
