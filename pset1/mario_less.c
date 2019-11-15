// This program asks the user to input the height and then prints a half pyramid to that height
#include <stdio.h>
#include <cs50.h>
 
int main(void)
{
    // Declaring variables
    int height, row, space, hash;
 
    // Asks user to input an integer 1 through 8
    // While the user input is incorrect it will continue to ask the user for input
    do
    {
        height = get_int("Enter height (1 through 8): ");
    }
    while (height < 1 || height > 8);
 
    // Print new row as long as the number of rows is less than the height
    for (row = 0; row < height; row++) 
    {   // Subtract one space from each row
        for (space = height - row; space > 1; space--)
        {   // Print a space
            printf(" ");
        } 
        // Add one hash to each row 
        for (hash = 1; hash <= row + 1; hash++)
        
        {   // Print a hash 
            printf("#");
        }
        // Print a new line
        printf("\n");    
    }
    return 0;
}