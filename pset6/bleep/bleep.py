# This program will censor a message using the provided banned words text file

from cs50 import get_string
from sys import argv, exit


def main():
    # Make sure there are exactly 2 command line arguments. If not, exit.
    if len(argv) == 2:

        # Open and read the banned words text file
        with open(argv[1]) as f:
            banned = f.read().split('\n')

        # Get a message from the user
        message_in = get_string("What message do you want to censor?\n").split()

        # Create and print the censored message
        message_out = []
        for word in message_in:
            if word.lower() in banned or word.upper() in banned:
                message_out.append('*' * len(word))
            else:
                message_out.append(word)
        print(' '.join(message_out))

    else:
        print("Usage: python bleep.py dictionary")
        exit(1)


if __name__ == "__main__":
    main()