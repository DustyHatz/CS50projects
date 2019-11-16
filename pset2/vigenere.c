// This program will encrypt a text message using the Vigenere Cipher!
// By: Dustin Hatzenbuhler

#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

// Accept user input at runtime
int main(int argc, string argv[])
{

    // User must enter exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./vigenere keyword\n");
        return 1;
    }

    // Store the string length of the command-line argument
    int keyLen = strlen(argv[1]);

    // Make sure the command-line argument does not include any numeric values
    for (int i = 0; i < keyLen; i++)
    {
        if (isalpha( argv[1][i]) == false)
        {
            printf("Keyword cannot include numeric values!\n");
            return 1;
        }
    }

    // Ask user to enter the original message
    string plainText = get_string("Original Message: ");

    // Print the encrypted message as "Ciphertext"
    printf("ciphertext: ");

    // Iterate through the original message
    for (int i = 0, j = 0, cipherText = 0, n = strlen(plainText); i < n; i++)
    {
        char ch = plainText[i];

        // Only apply the jth character of key to plainText if the character in plainText is alphabetical
        char key = argv[1][(j) % keyLen];

        // For characters in key,  'A' and 'a' is 0, 'B' and 'b' is 1, … , and 'Z' and 'z' is 25
        if (isupper(key))
        {
            key -= 65;
        }
        else if (islower(key))
        {
            key -= 97;
        }
        if (isupper(ch))
        {
            cipherText = (ch + key - 65) % 26 + 65;
            j++;
        }
        else if (islower(ch))
        {
            cipherText = (ch  + key - 97) % 26 + 97;
            j++;
        }

        // Preserve any characters in the plainText if they are not 'a'-'z' or 'A'-'Z'
        else
        {
            cipherText = ch;
        }

        // Print the characters of the cipherText
        printf("%c", cipherText);
    }
    printf("\n");
}