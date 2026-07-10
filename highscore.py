
import json
import os

FILE_NAME = "highscore.json"

def load_high_score():

    if not os.path.exists(FILE_NAME):
        return 0

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)
            return data.get("high_score", 0)

    except (json.JSONDecodeError, KeyError):
        return 0


def save_high_score(score):

    with open(FILE_NAME, "w") as file:
        json.dump(
            {"high_score": score},
            file,
            indent=4
        )
