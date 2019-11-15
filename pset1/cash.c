//This program calculates the minumum number of coins needed to provide the amount of change owed.

#include <cs50.h>
#include <math.h>
#include <stdio.h>

int main(void)
{
    // Declare variables
    float changeOwed = .41;
    int numOfCoins = 0;
    int remainder = 0;

    // Get a float input from the user as long as input is greater than 0
    do
    {
        changeOwed = get_float("Amount of change owed: ");
    }
    while (changeOwed <= 0);

    // Convert float changeOwed to integer cents
    int cents = round(changeOwed * 100);

    // Find the remainder of cents. (How many times does 25 go into cents?)
    remainder = cents % 25;

    // Calculate the number of coins (quarters) used
    numOfCoins += (cents - remainder) / 25;

    // Update the remaining amount of cents
    cents = remainder;

    // Find the remainder of cents. (How many times does 10 go into cents?)
    remainder = cents % 10;

    // Calculate the number of coins (dimes) used
    numOfCoins += (cents - remainder) / 10;

    // Update the remaining amount of cents
    cents = remainder;

    // Find the remainder of cents. (How many times does 5 go into cents?)
    remainder = cents % 5;

    // Calculate the number of coins (nickels) used
    numOfCoins += (cents - remainder) / 5;

    // Update the remaining amount of cents
    cents = remainder;

    // Find the remainder of cents. (How many times does 1 go into cents?)
    remainder = cents % 1;

    // Calculate the number of coins (pennies) used
    numOfCoins += (cents - remainder) / 1;
    
        
       // Print the total number of coins used
       printf("Number of coins used: %d\n", numOfCoins);
    
   return 0;
}