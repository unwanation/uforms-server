from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from . import Base
from .form import Form


class Entry(Base):
    __tablename__ = "entries"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    form_id = mapped_column(ForeignKey("forms.id"))
    form: Mapped[Form] = relationship()
