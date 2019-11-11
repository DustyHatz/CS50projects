# This program builds a one sided pyramid to the height of the user input

from cs50 import get_int


# Create function for getting height from user


def get_height(prompt):
    while True:
        n = get_int(prompt)
        if n > 0 and n < 9:
            return n


# Get height from user
height = get_height("Height: ")

# Build pyramid
for i in range(height):
    for j in range((height - 1) - i):
        print(" ", end="")
    for k in range(i + 1):
        print("#", end="")
