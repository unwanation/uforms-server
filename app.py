import sys
import uvicorn
from getopt import getopt, GetoptError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db
from .models import Form, Question, Variant, Entry, Answer, AnswerVariant
from . import routes

VERSION = "1.0.1"
API_VERSION = "1"

app = FastAPI(title="uFormsAPI", root_path=f"/api/v{API_VERSION}", version=VERSION)

ORIGINS = [
    "http://localhost",
    "http://127.0.0.0",
    "http://127.0.0.0:3000",
    "http://127.0.0.0:5000",
    "http://localhost:3000",
    "http://localhost:5500",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=ORIGINS,
    allow_credentials=True,
    allow_methods=["post", "get"],
    allow_headers=["*"],
)


def main(argv):
    HOST = "localhost"
    PORT = 8000
    DEBUG = False

    try:
        opts, args = getopt(argv, "d", ["host=", "port="])
    except GetoptError:
        print("server.app --host <host> --port <port>")
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

    create_db()

    uvicorn.run(
        "server.app:app",
        host=HOST,
        port=PORT,
        reload=DEBUG,
    )


if __name__ == "__main__":
    main(sys.argv[1:])
