// This program will print a two sided pyramid to a use specified hieght

#include <stdio.h>
#include <cs50.h>

int main(void)
{
    // Declaring variables
    int height, rows, space, hash;
 
    // Asks user to input an integer 1 through 8
    // While the user input is incorrect it will continue to ask the user for input
    do
    {
        height = get_int("Enter height (1 through 8): ");
    }
    while (height < 1 || height > 8);

    // Print new row as long as the number of rows is less than the height
    for (rows = 0; rows < height; rows++)
    {
        // Subtract one space from each row
        for (space = height - rows; space > 1; space--)
        {
            // Print a space
            printf(" ");
        }
        // Add an additional hash to each row
        for (hash = 1; hash <= rows + 1; hash++)
        {
            // Print a hash
            printf("#");
        }
        // Add two spaces to each row
        for (space = 2; space > 0; space--)
        {
            // Print a space
            printf(" ");
        }
        // Add an asdditional hash to each row
        for (hash = 1; hash <= rows + 1; hash++)
        {
            // Print a hash
            printf("#");
        }
        printf("\n");
    }
    return 0;
}