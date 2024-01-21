import random


class StringDatabase:
    def __init__(self):
        self.words = set()
        self.load_words_from_file(self)
        self.words = list(self.words)

    @staticmethod
    def load_words_from_file(self, file_path="four_letters.txt"):
        try:
            with open(file_path, 'r') as file:
                for line in file:
                    # Assuming each line contains words separated by spaces
                    words_in_line = line.strip().split()

                    # Filter out words that are not exactly four letters long
                    four_letter_words = [word.lower() for word in words_in_line if len(word) == 4]

                    # Add the four-letter words to the set
                    self.words.update(four_letter_words)
        except FileNotFoundError:
            print(f"Error: File '{file_path}' not found.")
        except Exception as e:
            print(f"Error: {e}")

    def get_random_word(self):
        if not self.words:
            raise ValueError("No words loaded from the file.")
        return random.choice(self.words)
