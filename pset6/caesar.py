# This program will creat a "Caesar Cipher"
# User must enter a key (positive integer) and a message to encrypt

from cs50 import get_string
from sys import argv, exit

# Check for exacctly one command line argument and make sure it is a positive integer. If not, exit.
if len(argv) == 2 and argv[1].isdigit():

    # Convert command line argument to an integer
    key = int(argv[1])

    # Check to make sure the key is a positive integer. If not, exit.
    if key > 0:

        # Promt user for original message
        message = get_string("Message: ")

        # Create empty string for ciphertext
        ciphertext = ""

        # Iterate over the entire original message
        for i in range(len(message)):
            char = message[i]
            # Keep puncuation the same
            if not char.isalpha():
                ciphertext += char
            # Shift uppercase and lowercase letters by amount of the key
            elif char.isupper():
                ciphertext += chr((ord(char) + key - 65) % 26 + 65)
            else:
                ciphertext += chr((ord(char) + key - 97) % 26 + 97)

        # Print the original message and the encrypted message
        print("plaintext: " + message)
        print("ciphertext: " + ciphertext)

    else:
        print("Usage: python caesar.py k\n")
        exit(1)
else:
    print("Usage: python caesar.py k\n")
    exit(1)