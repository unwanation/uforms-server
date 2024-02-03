from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from . import Base
from .question import Question


class Variant(Base):
    __tablename__ = "variants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    name: Mapped[str]

    question_id = mapped_column(ForeignKey("questions.id"))
    question: Mapped[Question] = relationship()

