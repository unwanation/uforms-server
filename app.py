import sys
import uvicorn
from getopt import getopt, GetoptError
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_db
from .models import Form, Question, Variant, Entry, Answer, AnswerVariant
from . import routes

VERSION = "1.0.0"

app = FastAPI(title="uFormsAPI", root_path=f"/api/v{VERSION}", version=VERSION)


def main(argv):
    HOST = "localhost"
    PORT = 8000
    ORIGIN = "localhost:4000"
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
                ORIGIN = arg

    ORIGINS = [f"http://{ORIGIN}"]

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
