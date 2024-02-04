from sqlmodel import SQLModel, create_engine, Session, select
from .models import Form, Question, Variant, Entry, Answer, AnswerVariant

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url)


def create_db():
    SQLModel.metadata.create_all(engine)


def clear_db():
    with Session(engine) as session:
        for table in (Form, Question, Variant, Entry, Answer, AnswerVariant):
            for e in session.exec(select(table)).all():
                session.delete(e)

        session.commit()
