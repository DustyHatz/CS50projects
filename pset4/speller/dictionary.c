// Implements a dictionary's functionality

#include <stdlib.h>
#include <math.h>
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <string.h>


#include "dictionary.h"

// Represents number of buckets in a hash table
#define N 26

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
}
node;

// Represents a hash table
node *hashtable[N];

// Hashes word to a number between 0 and 25, inclusive, based on its first letter
unsigned int hash(const char *word)
{
    return tolower(word[0]) - 'a';
}

// Declare global vairable to count size of dictionary
int dictionarySize = 0;

// Loads dictionary into memory, returning true if successful else false
bool load(const char *dictionary)
{
    // Initialize hash table
    for (int i = 0; i < N; i++)
    {
        hashtable[i] = NULL;
    }

    // Open dictionary
    FILE *file = fopen(dictionary, "r");
    if (file == NULL)
    {
        unload();
        return false;
    }

    // Buffer for a word
    char word[LENGTH + 1];

    // Insert words into hash table
    while (fscanf(file, "%s", word) != EOF)
    {
        // TODO
        // Increase dictionary size
        dictionarySize++;

        // Allocate memory for new word
        node *newWord = malloc(sizeof(node));

        // Put word in the new node
        strcpy(newWord->word, word);

        // Find what index of the array the word should go in
        int index = hash(word);

        // If hashtable is empty at index, insert
        if (hashtable[index] == NULL)
        {
            hashtable[index] = newWord;
            newWord->next = NULL;
        }

        // If hashtable is not empty at index, append
        else
        {
            newWord->next = hashtable[index];
            hashtable[index] = newWord;
        }
    }

    // Close dictionary
    fclose(file);

    // Indicate success
    return true;
}

// Returns number of words in dictionary if loaded else 0 if not yet loaded
unsigned int size(void)
{
    // TODO
    // If dictionary is loaded, return number of words
    if (dictionarySize > 0)
    {
        return dictionarySize;
    }

    // If dictionary hasn't been loaded, return 0
    else
    {
        return 0;
    }
}

// Returns true if word is in dictionary else false
bool check(const char *word)
{
    // TODO
    // Creates a tmp variable that stores a lower-cased version of the word
    char tmp[LENGTH + 1];
    int len = strlen(word);
    for (int i = 0; i < len; i++)
    {
        tmp[i] = tolower(word[i]);
    }
    tmp[len] = '\0';

    // Find what index of the array the word should be in
    int index = hash(tmp);

    // If hashtable is empty at index, return false
    if (hashtable[index] == NULL)
    {
        return false;
    }

    // Create cursor to compare to word
    node *cursor = hashtable[index];

    // If hashtable is not empty at index iterate through words and compare
    while (cursor != NULL)
    {
        if (strcmp(tmp, cursor->word) == 0)
        {
            return true;
        }
        cursor = cursor->next;
    }

    // If the word is not found return false
    return false;
}

// Unloads dictionary from memory, returning true if successful else false
bool unload(void)
{
    // TODO
    // Create a variable to go through index
    int index = 0;

    // Iterate through hashtable array
    while (index < N)
    {
        // If hashtable is empty at index go to next index
        if (hashtable[index] == NULL)
        {
            index++;
        }

        // If hashtable is not empty iterate through nodes and start freeing
        else
        {
            while (hashtable[index] != NULL)
            {
                node *cursor = hashtable[index];
                hashtable[index] = cursor->next;
                free(cursor);
            }

            // Once hashtable is empty at index go to next index
            index++;
        }
    }

    // Return true if successful
    return true;
}
