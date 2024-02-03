from sqlalchemy.orm import declarative_base

Base = declarative_base()

from .form import Form
from .question import Question
from .variant import Variant
from .entry import Entry
from .answer import Answer
from .answer_variant import AnswerVariant
