import json
import os
import random
import string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WORDS_FILE = os.path.join(BASE_DIR, "words.json")
MAX_LIVES = 3

STAGES = [
    r"""
  +---+
  |   |
      |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
      |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
  |   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|   |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========""",
    r"""
  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========""",
]


class Hangman:
    def __init__(self, word, max_lives=MAX_LIVES):
        self.word = word.lower()
        self.max_lives = max_lives
        self.lives = max_lives
        self.guessed = set()
        self.wrong = []

    def masked_word(self):
        return " ".join(c if c in self.guessed else "_" for c in self.word)

    def guess(self, letter):
        if letter in self.guessed or letter in self.wrong:
            return "repeat"
        if letter in self.word:
            self.guessed.add(letter)
            return "correct"
        self.wrong.append(letter)
        self.lives -= 1
        return "wrong"

    def hint(self):
        hidden = [c for c in set(self.word) if c not in self.guessed]
        if self.lives <= 1 or not hidden:
            return None
        letter = random.choice(hidden)
        self.guessed.add(letter)
        self.lives -= 1
        return letter

    def is_won(self):
        return all(c in self.guessed for c in self.word)

    def is_lost(self):
        return self.lives <= 0

    def stage(self):
        return STAGES[self.max_lives - self.lives]


def load_words(filename):
    with open(filename, encoding="utf-8") as f:
        return json.load(f)


def get_number(prompt, low, high):
    while True:
        value = input(prompt).strip()
        if value.isdigit() and low <= int(value) <= high:
            return int(value)
        print(f"Please type a number from {low} to {high}.")


def choose_category(words):
    categories = list(words.keys())
    print("\nChoose a category:")
    for i, name in enumerate(categories, start=1):
        print(f"  {i}. {name}")
    print(f"  {len(categories) + 1}. Quit")
    choice = get_number("Your choice: ", 1, len(categories) + 1)
    if choice == len(categories) + 1:
        return None
    return categories[choice - 1]


def play_round(word):
    game = Hangman(word)
    print("\nGuess the word! Type a letter, 'hint' (costs one life), or 'quit'.")

    while not game.is_won() and not game.is_lost():
        print(game.stage())
        print("Word:", game.masked_word())
        wrong_letters = " ".join(game.wrong) or "none"
        print(f"Lives: {game.lives}   Wrong letters: {wrong_letters}")

        entry = input("Your guess: ").strip().lower()

        if entry == "quit":
            print("You left the round.")
            return None

        if entry == "hint":
            letter = game.hint()
            if letter is None:
                print("No hint available right now.")
            else:
                print(f"Hint: the word contains '{letter}'. You lost one life.")
            continue

        if len(entry) != 1 or entry not in string.ascii_lowercase:
            print("Please type a single letter from a to z.")
            continue

        result = game.guess(entry)
        if result == "repeat":
            print("You already tried that letter.")
        elif result == "correct":
            print("Good guess!")
        else:
            print("Wrong guess!")

    print(game.stage())
    if game.is_won():
        print(f"\nYou won! The word was '{game.word}'.")
    else:
        print(f"\nYou lost! The word was '{game.word}'.")
    return game.is_won()


def main():
    try:
        words = load_words(WORDS_FILE)
    except (FileNotFoundError, json.JSONDecodeError):
        print("Could not load words.json. Check that the file exists and is correct.")
        return

    print("Welcome to Hangman!")
    wins = 0
    rounds = 0

    while True:
        category = choose_category(words)
        if category is None:
            print("Thanks for playing!")
            break

        word = random.choice(words[category])
        result = play_round(word)
        if result is None:
            print("Thanks for playing!")
            break

        rounds += 1
        if result:
            wins += 1

        print(f"Your record: {wins} won out of {rounds} played.")
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break


if __name__ == "__main__":
    main()