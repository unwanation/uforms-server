import crud
from pydantic import BaseModel
from uvicorn import run
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


class Entry(BaseModel):
    form_id: int
    answers: list[dict]


HOST = "localhost"
ORIGINS = ["http://localhost", "http://localhost:4000"]
VERSION = "0.2"

app = FastAPI(title="FormsAPI", root_path=f"/api/v{VERSION}", version=VERSION)


app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return "A mne amerikanskiye burgers dorozhe rootovogo routa"


@app.get("/forms")
def get_forms():
    return crud.get_forms()


@app.get("/forms/{id}")
def get_form(id: int):
    return {
        "id": id,
        "questions": crud.get_questions_by_form(id),
        "variants": crud.get_variants_by_question(id),
    }


@app.post("/entry")
def create_entry(entry: Entry):
    if not entry.answers:
        raise ValueError("Entry must have answers")
    id = crud.get_entry_count() + 1
    crud.create_entry(form_id=entry.form_id)
    for answer in entry.answers:
        if "body" in answer:
            crud.create_answer(answer.question_id, id, body=answer.body)
        elif "variant_id" in answer:
            crud.create_answer(answer.question_id, id, variant_id=answer.variant_id)
        else:
            raise ValueError("Answer must have either body or variant_id")


if __name__ == "__main__":
    run(
        "main:app",
        host=HOST,
        port=8000,
        reload=True,
    )
