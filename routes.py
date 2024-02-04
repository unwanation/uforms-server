from uuid import uuid4
from sqlmodel import Session, select
from .app import app as router
from .database import engine
from .models import Form, Question, Variant, Entry, Answer, AnswerVariant
from .network_models import FormQuery, FormResp, EntryQuery


@router.get("/")
async def root():
    return "A mne amerikanskiye burgers dorozhe rootovogo routa"


@router.get("/forms")
def get_forms():
    with Session(engine) as session:
        return session.exec(select(Form)).all()


@router.get("/forms/{id}")
def get_form(id: str):
    with Session(engine) as session:
        form = session.get(Form, id)
        return {
            "name": form.name,
            "questions": form.questions,
            "variants": [i.variants for i in form.questions],
        }


@router.post("/new-form")
def create_form(form: FormQuery) -> FormResp:
    uuid = str(uuid4())

    with Session(engine) as session:
        session.add(Form(uuid=uuid, name=form.name))
        qid = len(session.exec(select(Question)).all()) + 1
        for question in form.questions:
            session.add(
                Question(
                    name=question.name,
                    description=question.description,
                    allows_multiple_answer=question.allows_multiple_answer,
                    form_id=uuid,
                )
            )
            for variant in question.variants:
                session.add(Variant(name=variant, question_id=qid))
            qid += 1
        session.commit()

    return {"name": form.name, "uuid": uuid}


@router.post("/new-entry")
def create_entry(entry: EntryQuery):
    with Session(engine) as session:
        id = len(session.exec(select(Entry)).all()) + 1
        aid = len(session.exec(select(Answer)).all()) + 1
        session.add(Entry(form_id=entry.form_id))
        for answer in entry.answers:
            session.add(
                Answer(body=answer.body, question_id=answer.question_id, entry_id=id)
            )
            for i in answer.answer_variants:
                session.add(AnswerVariant(variant_id=i, answer_id=aid))

            aid += 1
        session.commit()
