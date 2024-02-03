from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from . import Base
from .form import Form


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]
    description: Mapped[str | None]
    allows_multiple_answer: Mapped[bool] = mapped_column(default=False)

    form_id = mapped_column(ForeignKey("forms.id"))
    form: Mapped[Form] = relationship()
