class Game:
    total_games = 0  # Class variable to keep track of the total number of games

    def __init__(self, word_to_guess):
        Game.total_games += 1
        self.game_number = Game.total_games
        self.word_to_guess = word_to_guess
        self.current_status = list('----')
        self.letters_guessed = set()
        self.bad_guesses = 0
        self.missed_letters = 0
        self.score = 0.00
        self.status = None  # 'Success' or 'Gave up'

    def update_game_state(self, guessed_letter):
        self.letters_guessed.add(guessed_letter)

        correct_guess = False  # Flag to check if the guessed letter is correct

        for i, letter in enumerate(self.word_to_guess):
            if letter == guessed_letter:
                self.current_status[i] = guessed_letter
                correct_guess = True

        if correct_guess:
            print(f"Good guess! The letter '{guessed_letter}' is in the word.")
        else:
            # Guessed letter is not in the word
            self.missed_letters += 1
            print(f"Oops! The letter '{guessed_letter}' is not in the word.")
