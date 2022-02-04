def parser():
    file = open("/etc/dictionaries-common/words", "r", encoding="utf-8")
    words = open("../data/.words", "w", encoding="utf-8")

    for word in file.readlines():
        if len(word) == 6 and word[:-1].isalpha():
            words.write(word)

    file.close()
    words.close()


if __name__ == "__main__":
    parser()
