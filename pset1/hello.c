// This program takes a users name as input and prints a message using that name

#include <stdio.h>
#include <cs50.h>

int main(void)
{
    string name = get_string("What's your name?\n");
    printf("hello, %s\n", name);
}