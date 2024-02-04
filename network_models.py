from .models import Form, Question, Variant, Entry, Answer, AnswerVariant
from pydantic import BaseModel


class QuestionQuery(BaseModel):
    name: str
    description: str | None
    allows_multiple_answer: bool = False
    variants: list[str]


class FormQuery(BaseModel):
    name: str
    questions: list[QuestionQuery]


class FormResp(BaseModel):
    uuid: str
    name: str


class AnswerQuery(BaseModel):
    body: str | None
    question_id: int
    answer_variants: list[int]


class EntryQuery(BaseModel):
    form_id: str
    answers: list[AnswerQuery]
