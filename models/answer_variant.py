from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey

from . import Base
from .variant import Variant
from .answer import Answer


class AnswerVariant(Base):
    __tablename__ = "answer_variants"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True, index=True)

    variant_id = mapped_column(ForeignKey("variants.id"))
    variant: Mapped[Variant] = relationship()

    answer_id = mapped_column(ForeignKey("answers.id"))
    answer: Mapped[Answer] = relationship()
