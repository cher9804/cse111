import os

import random

os.system("cls" if os.name == "nt" else "clear")

def main():
    numbers = [16.2, 75.1, 52.3]
    print(numbers)
    append_random_numbers(numbers)
    print(numbers)
    append_random_numbers(numbers, 3)
    print(numbers)
    words_list = []
    append_random_words(words_list, 6)
    print(words_list)


def append_random_numbers(numbers_list, quantity=1):
    """
    Append a quantity of random new numbers to a list.
    Parameters:
    numbers_lists: list where numbers will be appended
    quantity: default = 1, integer. Number of new items to be added to the list
    Return:
    Nothing, appends new numbers to a list

    """
    for _ in range(quantity):
        random_number = random.uniform(0, 100)
        rounded = round(random_number, 1)
        numbers_list.append(rounded)

def append_random_words (words_list, quantity=1):
    """
    Append a quantity of random new words to a list.
    Parameters:
    numbers_lists: list where words will be appended
    quantity: default = 1, integer. Number of new items to be added to the list
    Return:
    Nothing, appends new numbers to a list

    """
    words = ["lol", "test", "queso", "run"]
    for _ in range(quantity):
        random_word = random.choice(words)
        words_list.append(random_word)



if __name__ == "__main__":
    main()


