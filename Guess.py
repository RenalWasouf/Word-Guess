from StringDatabase import StringDatabase
from Game import Game
import os


class Guess:
    string_db = StringDatabase()

    def __init__(self, mode):
        self.current_game = None
        self.games = []
        self.mode = mode

    def start_new_game(self):
        self.current_game = Game(self.string_db.get_random_word())
        self.display_menu()

    def display_menu(self):
        # Clear the screen
        os.system('clear' if os.name == 'posix' else 'cls')
        # Display the game title
        print("++\n++ The great guessing game\n++\n")
        if self.mode == 1:
            print(f"Current Word: {self.current_game.word_to_guess}")
        # Display the current guess
        print(f"Current Guess: {''.join(self.current_game.current_status)}")
        # Display the letters guessed
        print(f"Letters guessed: {', '.join(self.current_game.letters_guessed)}")
        # Display the menu options
        print("\ng = guess, t = tell me, l for a letter, and q to quit")

        self.get_user_input()

    def get_user_input(self):
        user_input = input("Enter your choice: ")

        if user_input.lower() == 'g':
            self.handle_word_guess()
        elif user_input.lower() == 'l':
            self.handle_letter_guess()
        elif user_input.lower() == 't':
            self.handle_give_up()
        elif user_input.lower() == 'q':
            self.handle_quit()
        else:
            print("Invalid choice. Please try again.")
            self.get_user_input()

    def handle_letter_guess(self):
        guessed_letter = input("Enter the letter to guess: ").lower()

        if self.current_game:
            while guessed_letter in self.current_game.letters_guessed or len(guessed_letter) > 1:
                # Letter has already been guessed or is not a letter
                if guessed_letter in self.current_game.letters_guessed:
                    print(f"You already guessed the letter '{guessed_letter}'.")
                elif len(guessed_letter) > 1:
                    print("You entered more than one letter.")

                guessed_letter = input("Please enter another letter:").lower()

            self.current_game.update_game_state(guessed_letter)

            # Check if the word has been fully guessed
            if '-' not in self.current_game.current_status:
                print(f"Congratulations! You guessed the word: {''.join(self.current_game.current_status)}")
                self.calculate_score()
                self.games.append(self.current_game)  # Store completed game
                i = input("Press Enter to continue...")
                self.start_new_game()
                return

            i = input("Press Enter to continue...")
            self.display_menu()

    def handle_word_guess(self):
        guessed_word = input("Enter the word to guess: ").lower()
        if self.current_game:
            # Check if the user's guess matches the selected word
            if guessed_word == self.current_game.word_to_guess:
                print("Congratulations! You guessed the word correctly!")

                # Add each letter from the word to the guessed letters set to
                # keep calculations accurate
                for letter in self.current_game.word_to_guess:
                    self.current_game.letters_guessed.add(letter)

                self.calculate_score()
                self.games.append(self.current_game)
                i = input("Press Enter to continue...")
                self.start_new_game()
            else:
                print("Oops! Your guess was incorrect.")
                self.current_game.bad_guesses += 1
                i = input("Press Enter to continue...")
                self.start_new_game()

    def handle_give_up(self):
        if self.current_game:
            self.current_game.status = 'Gave up'
            self.calculate_score()
            self.games.append(self.current_game)  # Store completed game
            print(f"Too bad! The word was {self.current_game.word_to_guess}")
            i = input("Press Enter to continue...")
            self.start_new_game()

    def handle_quit(self):
        # Handle quitting the game
        decision = input("This round will not be scored. Do you still wish to quit? (y/n) ")
        while decision != 'y' or decision != 'n':
            if decision == 'n':
                self.display_menu()
            elif decision == 'y':
                self.display_summary()
                exit()
            else:
                decision = input("Invalid option. Please enter 'y' for YES, or 'n' for NO: ")

    def calculate_score(self):
        # Calculate the score based on the current state of the game
        total_points = sum(self.frequency(letter) for letter in self.current_game.word_to_guess if
                           letter in self.current_game.letters_guessed)
        # Get the set of uncovered letters
        uncovered_letters = set(letter for letter, guess_char in
                                zip(self.current_game.word_to_guess, self.current_game.current_status)
                                if guess_char == '-')
        # Sum the frequencies of uncovered letters
        sum_of_uncovered = sum(self.frequency(letter) for letter in uncovered_letters)
        points_per_guess = total_points / max(1, len(self.current_game.letters_guessed))
        penalty = ((0.1 * self.current_game.bad_guesses) * total_points)

        self.current_game.score = (points_per_guess - penalty - sum_of_uncovered)

    def display_summary(self):
        os.system('clear' if os.name == 'posix' else 'cls')
        print("Game Summary:")
        total_score = 0.00
        for i, game in enumerate(self.games, start=1):
            result = 'Success' if game.status is None else 'Gave up'
            print(f"Game {i}: Word: {game.word_to_guess}, Status: {result}, "
                  f"Bad Guesses: {game.bad_guesses}, Missed Letters: {game.missed_letters}, "
                  f"Score: {game.score:.2f}")
            total_score += game.score

        print(f"\nFinal Score: {total_score:.2f}")

    @staticmethod
    def frequency(letter):
        # Helper method to get the frequency of a letter
        frequencies = {'a': 8.17, 'b': 1.49, 'c': 2.78, 'd': 4.25, 'e': 12.70, 'f': 2.23, 'g': 2.02, 'h': 6.09,
                       'i': 6.97, 'j': 0.15, 'k': 0.77, 'l': 4.03, 'm': 2.41, 'n': 6.75, 'o': 7.51, 'p': 1.93,
                       'q': 0.10, 'r': 5.99, 's': 6.33, 't': 9.06, 'u': 2.76, 'v': 0.98, 'w': 2.36, 'x': 0.15,
                       'y': 1.97, 'z': 0.07}

        return round(float(frequencies.get(letter, 0.0)), 2)
