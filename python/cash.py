# This program will get an amount of change owed from the user and return the minimum number of coins needed
from cs50 import get_float


# Define main program function
def main():
    # Get amount of change owed from user
    change_owed = get_positive_float("Amount of change owed: ")
    # Convert to cents
    cents = int(change_owed * 100)
    # Calculate miminum number of coins
    coins = get_coins(cents)
    # Print the minimum number of coins
    print(coins)


# Define the function for getting a non negative float
def get_positive_float(prompt):
    while True:
        n = get_float(prompt)
        if n >= 0:
            return n


# Define function to calculate the minimum number of coins
def get_coins(cents):
    quarters = cents // 25
    dimes = (cents % 25) // 10
    nickels = ((cents % 25) % 10) // 5
    pennies = ((cents % 25) % 10) % 5
    return quarters + dimes + nickels + pennies


# Run main program function
main()