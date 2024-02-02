import sqlalchemy.orm as orm
import database as db


def create_form(name: str):
    db.stack.append(db.Form(name=name))


def create_question(
    name: str,
    description: str,
    form_id: int,
    multiple_answer: bool = False,
    variants: list[str] = [],
):
    db.stack.append(
        db.Question(
            name=name,
            description=description,
            multiple_answer=multiple_answer,
            form_id=form_id,
        )
    )

    for i in variants:
        create_variant(i, db.stack[-1].id)


def create_variant(name: str, question_id: int):
    db.stack.append(db.Variant(name=name, question_id=question_id))


def create_entry(form_id: int):
    db.stack.append(db.Entry(form_id=form_id))


def create_answer(
    question_id: int, entry_id: int, body: str | None = None, variant_id=None
):
    db.stack.append(
        db.Answer(
            body=body, variant_id=variant_id, question_id=question_id, entry_id=entry_id
        )
    )


def get_forms():
    with orm.Session(bind=db.engine) as session:
        return session.query(db.Form).all()


def get_questions():
    with orm.Session(bind=db.engine) as session:
        return session.query(db.Question).all()


def get_variants():
    with orm.Session(bind=db.engine) as session:
        return session.query(db.Variant).all()


def get_questions_by_form(id):
    with orm.Session(bind=db.engine) as session:
        return session.query(db.Question).filter(db.Question.form_id == id).all()


def get_variants_by_question(id):
    with orm.Session(bind=db.engine) as session:
        return session.query(db.Variant).filter(db.Variant.question_id == id).all()


def get_entry_count():
    with orm.Session(bind=db.engine) as session:
        return session.query(db.Entry).count()


def delete_answers():
    db.delete(db.Answer)
    db.delete(db.AnswerVariants)


db.commit()
