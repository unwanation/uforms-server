import json
from crud import create_form, create_question
from database import commit, clear


def load():
    with open("example.json") as f:
        res = json.loads(f.read())
        clear()

        i = 1
        for form in res["forms"]:
            create_form(form["name"])
            for question in form["questions"]:
                create_question(
                    question["name"],
                    question["description"],
                    i,
                    question["isMultiple"],
                    question["variants"],
                )
            i += 1

        commit()


if __name__ == "__main__":
    load()
    print("[fromjson] Done!")
