// This program creates a secret message by way of a "Caesar Cipher".
// By: Dustin Hatzenbuhler

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

// Take user input at runtime
int main(int argc, string argv[])
{
    // User must enter exactly one command-line argument
    if (argc == 2)
    {
        // Convert input to int "key" (atoi will return "0" if char or string is entered)
        int key = atoi(argv[1]);

        // Value of key must be greater than 0
        if (key > 0)
        {

            // Prompt user to enter the original message
            string plainText = get_string("plaintext: ");

            // Store the length of the message
            int plainLength = strlen(plainText);

            // Print ciphertext
            printf("ciphertext: ");

            // Iterate through the length of the message
            for (int j = 0; j < plainLength; j++)
            {
                // Check if characters are upper or lower case and convert
                if (islower(plainText[j]))
                {
                    int cipherText = ((((plainText[j] + key) - 'a') % 26) + 'a');
                    printf("%c", cipherText);
                }
                else if (isupper(plainText[j]))
                {
                    int cipherText = ((((plainText[j] + key) - 'A') % 26) + 'A');
                    printf("%c", cipherText);
                }
                else
                {
                    printf("%c", plainText[j]);
                }
            }
            //Successful program
            printf("\n");
            return 0;
        }
    }
    // Unsuccessful program
    printf("Usage: ./caesar key\n");
    return 1;
}