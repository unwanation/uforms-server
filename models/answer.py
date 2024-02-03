from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from . import Base
from .question import Question
from .entry import Entry


class Answer(Base):
    __tablename__ = "answers"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)
    body: Mapped[str | None]

    question_id = mapped_column(ForeignKey("questions.id"))
    question: Mapped[Question] = relationship()

    entry_id = mapped_column(ForeignKey("entries.id"))
    entry: Mapped[Entry] = relationship()
