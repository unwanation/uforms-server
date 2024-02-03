import uuid
from sqlmodel import Session, select
from .database import engine
from .models import Form, Question, Variant, Entry, Answer, AnswerVariant


def generate_uuid():
    return str(uuid.uuid4())


def create_form(name: str):
    uuid = generate_uuid()

    with Session(engine) as session:
        session.add(Form(uuid=uuid, name=name))
        session.commit()

    return uuid


def create_question(
    name: str, multiple: bool, form_id: str, description: str | None = None
):
    with Session(engine) as session:
        session.add(
            Question(
                name=name,
                description=description,
                allows_multiple_answer=multiple,
                form_id=form_id,
            )
        )
        session.commit()


def create_variant(name: str, question_id: int):
    with Session(engine) as session:
        session.add(
            Variant(
                name=name,
                question_id=question_id,
            )
        )
        session.commit()


def create_entry(form_id: str):
    with Session(engine) as session:
        id = len(session.exec(select(Entry)).all()) + 1
        session.add(Entry(form_id=form_id))
        session.commit()
    return id


def create_answer(
    entry_id: int,
    question_id: int,
    body: str | None = None,
    variants: list[int] | None = None,
):
    with Session(engine) as session:
        id = len(session.exec(select(Answer)).all()) + 1
        session.add(Answer(entry_id=entry_id, question_id=question_id, body=body))

        for variant in variants:
            session.add(AnswerVariant(variant_id=variant, answer_id=id))

        session.commit()


def clear_db():
    with Session(engine) as session:
        for table in [Form, Question, Variant, Entry, Answer, AnswerVariant]:
            for e in session.exec(select(table)).all():
                session.delete(e)

        session.commit()
