from sqlalchemy.orm import DeclarativeBase, relationship, Session
from sqlalchemy import Column, Integer, String, Boolean, create_engine, ForeignKey

stack = []


def commit():
    with Session(bind=engine) as session:
        session.add_all(stack)
        session.commit()
    stack.clear()


def delete(entity):
    with Session(bind=engine) as session:
        session.query(entity).delete()
        session.commit()


def clear():
    with Session(bind=engine) as session:
        session.query(Form).delete()
        session.query(Question).delete()
        session.query(Entry).delete()
        session.query(Answer).delete()
        session.query(Variant).delete()
        session.query(AnswerVariants).delete()

        session.commit()


class Base(DeclarativeBase):
    pass


class Form(Base):
    __tablename__ = "forms"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)


class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    multiple_answer = Column(Boolean, default=False)

    form_id = Column(ForeignKey("forms.id"))
    form = relationship("Form")


class Variant(Base):
    __tablename__ = "variants"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    question_id = Column(ForeignKey("questions.id"))
    question = relationship("Question")


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, autoincrement=True)

    form_id = Column(ForeignKey("forms.id"))
    form = relationship("Form")


class Answer(Base):
    __tablename__ = "answers"
    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(String)

    question_id = Column(ForeignKey("questions.id"))
    question = relationship("Question")

    entry_id = Column(ForeignKey("entries.id"))
    entry = relationship("Entry")


class AnswerVariants(Base):
    __tablename__ = "answer_variants"
    id = Column(Integer, primary_key=True, autoincrement=True)
    variant_id = Column(ForeignKey("variants.id"))
    variant = relationship("Variant")
    answer_id = Column(ForeignKey("answers.id"))
    answer = relationship("Answer")


engine = create_engine("sqlite:///store.db")

Base.metadata.create_all(bind=engine)
print("[Database] Created!")
