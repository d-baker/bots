from tweeter import tweet

def drowyreve():
    current_word = ""
    with open ("resources/drowyreve.txt") as fp:
        current_word = fp.readline().strip().decode("utf-8")
    tweet(current_word[::-1])
    # if tweeting fails the current word shouldn't get deleted
    with open("resources/drowyreve.txt", "r") as fin:
        words = fin.read().splitlines(True)
    with open("resources/drowyreve.txt", "w") as fout:
        fout.writelines(words[1:])

if __name__ == "__main__":
    drowyreve()
