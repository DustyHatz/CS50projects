// This program will recover deleted jpegs from a memory card
// By: Dustin Hatzenbuhler

#include <stdio.h>
#include <stdlib.h>

int main(int argc, char *argv[])
{
    // Make sure exactly one command-line argument is given
    if (argc != 2)
    {
        fprintf(stderr, "Usage: ./recover file\n");
        return 1;
    }

    // Open file on memory card
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        fprintf(stderr, "Could not open %s.\n", argv[1]);
        return 2;
    }

    // Declare global variables
    unsigned char *buffer = malloc(512);
    char filename[9];
    int counter = 0;
    FILE *img = NULL;

    while (fread(buffer, 512, 1, file) == 1)
    {
        // Check jpeg header
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff &&
            (buffer[3] & 0xf0) == 0xe0)
        {
            // If a jpeg is already open, close it to start the next one
            if (counter > 0)
            {
                fclose(img);
            }

            sprintf(filename, "%03i.jpg", counter);
            img = fopen(filename, "w");

            // Check if the jpeg file was created, if not, return error
            if (img == NULL)
            {
                fclose(file);
                free(buffer);
                fprintf(stderr, "Could not create %s", filename);
                return 3;
            }
            // Increase counter by 1 for next jpeg
            counter++;
        }

        if (!counter)
        {
            continue;
        }

        fwrite(buffer, 512, 1, img);
    }

    // when memorycard ends, close all files
    fclose(file);
    fclose(img);
    free(buffer);
    return 0;
}