# This program builds a two sided pyramid to the height of the user input

from cs50 import get_int


# Create function for getting height from user


def get_height(prompt):
    while True:
        n = get_int(prompt)
        if n > 0 and n < 8:
            return n


# Get height from user
height = get_height("Height: ")

# Build pyramid
for i in range(height):
    print(' ' * (height - i - 1), end="")
    print('#' * (i + 1), end="")
    print('  ', end="")
    print('#' * (i + 1))
