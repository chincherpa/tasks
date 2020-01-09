a = "teststring"


def run():
    while True:
        action = input(">>  ")

        if action == "a":
            print(a)
        elif action == "neu":  # Show list of used tags
            a = "neuer Teststring"


if __name__ == "__main__":
    run()
