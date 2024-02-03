from .database import create_db
from .models import Form, Question, Variant, Entry, Answer, AnswerVariant
from .crud import *


def main():
    create_db()


if __name__ == "__main__":
    main()
