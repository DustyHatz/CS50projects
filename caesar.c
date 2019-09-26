#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    if (argc == 2)
    {        
        int key = atoi(argv[1]);
        printf("key: %d\n", key);
        
        if (isdigit(key) == false) {
            string plainText = get_string("plaintext: ");
            int plainLength = strlen(plainText);
            printf("plainText %s\n", plainText);
            printf("plainLength %d\n", plainLength);
            printf("ciphertext: ");
            for (int j = 0; j < plainLength; j++)
            {
                if (islower(plainText[j]))
                {
                    int cipherText = ((((plainText[j] + key) - 'a') % 26) + 'a');
                    printf("%c", cipherText);
                } else if(isupper(plainText[j])) {
                    int cipherText = ((((plainText[j] + key) - 'A') % 26) + 'A');
                    printf("%c", cipherText);
                } else {
                    printf("%c", plainText[j]);
                }
            }
            printf("\n");
            return 0;
        }
        printf("Usage: ./caesar key\n");
        return 1;   
    }
    printf("Usage: ./caesar key\n");
    return 1;
}


