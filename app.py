import sys
import uvicorn
from getopt import getopt, GetoptError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db
from .models import Form, Question, Variant, Entry, Answer, AnswerVariant
from . import crud

VERSION = "1.0"

app = FastAPI(title="FormsAPI", root_path=f"/api/v{VERSION}", version=VERSION)


def main(argv):
    HOST = "localhost"
    PORT = 8000
    ORIGIN_PORT = 4000
    DEBUG = False

    try:
        opts, args = getopt(argv, "d", ["host=", "port=", "origin="])
    except GetoptError:
        print("server.app --port <port> --origin_port <origin_port>")
        sys.exit(2)
    for opt, arg in opts:
        match opt:
            case "-d":
                DEBUG = True
                print("DEBUG MODE")
            case "--host":
                HOST = arg
            case "--port":
                PORT = arg
            case "--origin":
                ORIGIN_PORT = arg

    ORIGINS = [f"http://{HOST}", f"http://{HOST}:{ORIGIN_PORT}"]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["post", "get"],
        allow_headers=["*"],
    )

    create_db()

    uvicorn.run(
        "server.app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
    )


if __name__ == "__main__":
    main(sys.argv[1:])


@app.get("/")
async def root():
    return "A mne amerikanskiye burgers dorozhe rootovogo routa"


@app.get("/forms")
def get_forms():
    return crud.get_forms()


@app.get("/forms/{id}")
def get_form(id: int):
    return crud.get_form(id)


@app.post("/newform")
def create_form(form: Form):
    uuid = crud.create_form(form.name)


@app.post("/newentry")
def create_entry(entry: Entry):
    id = crud.create_entry(form_id=entry.form_id)
    for answer in entry.answers:
        crud.create_answer(
            answer.question_id, id, body=answer.body, variants=answer.answer_variants
        )
