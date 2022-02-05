import random
import json


def random_word(imported=True):
    """
    returns a random word
    """
    file = open(f"{(not imported) * '../'}data/words", "r", encoding="utf-8")
    wrd = random.choice(file.readlines())[:-1]
    file.close()
    return wrd.lower()


def evaluate_guess(guess, wrd):
    """
    takes the guess as an argument and returns a list indicating the truth values;
    that is, if the letter is in the word and the right place, the value of the
    letter is 2. if the letter is in the word but not in the right place, then the
    value is 1. if neither, the value is 0.
    """
    arr = [0, 0, 0, 0, 0]

    for i in range(5):
        if guess[i].lower() == wrd[i]:
            arr[i] = 2

        elif guess[i].lower() in wrd:
            arr[i] = 1

        else:
            arr[i] = 0

    return arr


def fetch_data(imported=True):
    file = open(f"{(not imported) * '../'}data/data.json", "r", encoding="utf-8")
    jsondata = json.loads(file.read())
    file.close()
    return f"total guesses: {jsondata['total guesses']}\n" \
           f"total games: {jsondata['total games']}\n" \
           f"total successful games: {jsondata['total successful']}\n" \
           f"total unsuccessful games: {jsondata['total unsuccessful']}\n" \
           f"success rate: {jsondata['success rate']}\n" \
           f"correct in:\n" \
           f"\t1 guess: {jsondata['correct in'][0]}\n" \
           f"\t2 guesses: {jsondata['correct in'][1]}\n" \
           f"\t3 guesses: {jsondata['correct in'][2]}\n" \
           f"\t4 guesses: {jsondata['correct in'][3]}\n" \
           f"\t5 guesses: {jsondata['correct in'][4]}\n" \
           f"\t6 guesses: {jsondata['correct in'][5]}"


def update_data(num, successful, imported=True):
    file = open(f"{(not imported) * '../'}data/data.json", "r", encoding="utf-8")
    jsondata = json.loads(file.read())
    file.close()

    jsondata["total games"] += 1
    jsondata["total successful"] += successful
    jsondata["total unsuccessful"] += not successful
    jsondata["success rate"] = "%" + str(jsondata["total successful"] * 100 / jsondata["total games"])

    if num != -1:
        jsondata["correct in"][num - 1] += 1
        jsondata["total guesses"] += (num)

    else:
        jsondata["total guesses"] += 6

    file = open(f"{(not imported) * '../'}data/data.json", "w", encoding="utf-8")
    json.dump(jsondata, file)
    file.close()


if __name__ == "__main__":
    """
    test
    """
    word = random_word(False)
    print(word)
    for i in range(6):
        guess = input()
        print(evaluate_guess(guess, word))
        if evaluate_guess(guess, word) == [2, 2, 2, 2, 2]:
            print("true")
            update_data(i+1, True, False)
            break



    print(word)

