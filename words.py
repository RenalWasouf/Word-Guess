from Guess import Guess
import argparse


def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='The Great Guessing Game')
    parser.add_argument('mode', choices=['play', 'test'], help='Choose the game mode: play or test')
    args = parser.parse_args()

    if args.mode == 'play':
        guess = Guess(0)
        guess.start_new_game()
    elif args.mode == 'test':
        # Run the game in test mode
        guess = Guess(1)
        guess.start_new_game()


if __name__ == '__main__':
    main()
