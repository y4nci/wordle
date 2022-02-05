"""
resets the data
"""

import json


def reset_data(imported=True):
    file = open(f"{(not imported) * '../'}data/data.json", "r", encoding="utf-8")
    jsondata = json.loads(file.read())
    file.close()

    jsondata["total games"] = 0
    jsondata["total successful"] = 0
    jsondata["total unsuccessful"] = 0
    jsondata["success rate"] = "%0"

    jsondata["correct in"] = [0, 0, 0, 0, 0, 0]
    jsondata["total guesses"] = 0

    file = open(f"{(not imported) * '../'}data/data.json", "w", encoding="utf-8")
    json.dump(jsondata, file)
    file.close()


if __name__ == "__main__":
    reset_data(False)

