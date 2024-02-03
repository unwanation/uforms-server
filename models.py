from sqlmodel import Field, Relationship, SQLModel


class Form(SQLModel, table=True):
    uuid: str = Field(primary_key=True, unique=True, index=True)
    name: str

    questions: list["Question"] = Relationship(back_populates="form")
    entries: list["Entry"] = Relationship(back_populates="form")


class Question(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str
    description: str | None
    allows_multiple_answer: bool = Field(default=False)

    form_id: str = Field(foreign_key="form.uuid")
    form: Form = Relationship(back_populates="questions")

    variants: list["Variant"] = Relationship(back_populates="question")


class Variant(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    name: str

    question_id: int = Field(foreign_key="question.id")
    question: Question = Relationship(back_populates="variants")


class Entry(SQLModel, table=True):
    id: int | None = Field(primary_key=True)

    form_id: str = Field(foreign_key="form.uuid")
    form: Form = Relationship(back_populates="entries")

    answers: list["Answer"] = Relationship(back_populates="entry")


class Answer(SQLModel, table=True):
    id: int | None = Field(primary_key=True)
    body: str | None

    question_id: int = Field(foreign_key="question.id")
    question: Question = Relationship()

    entry_id: int = Field(foreign_key="entry.id")
    entry: Entry = Relationship(back_populates="answers")


class AnswerVariant(SQLModel, table=True):
    id: int | None = Field(primary_key=True)

    variant_id: int = Field(foreign_key="variant.id")
    variant: Variant = Relationship()

    answer_id: int = Field(foreign_key="answer.id")
    answer: Answer = Relationship()
