// Harvard CS50 2020
// Program will create a "runoff election"
// Voters can vote for more than one candidate, ranking them in order of preference


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <cs50.h>
#include <math.h>

#define MAX 9

typedef struct
{
    string name;
    int votes;
    bool eliminated;
}
candidate;

candidate candidates[MAX];

int voter_count;
int candidate_count;
int preferences[MAX][MAX];
float winner_vote;

//void check_preference(void);
bool is_tie(int min);
bool vote(int voter, int rank, string name);
bool print_winner(void);
void tabulate(void);
int find_min(void);
void eliminate(int min);


int main(int argc, string argv[])
{
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    candidate_count = argc - 1;

    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }

    for (int i = 0; i < candidate_count ; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
        candidates[i].eliminated = false;
    }

    voter_count = get_int("Number of voters: ");

    winner_vote = voter_count / 2;

    int integer = winner_vote;

    if (winner_vote == integer)
    {
        winner_vote++;
    }
    else
    {
        winner_vote = ceil(winner_vote);
    }

    for (int i = 0; i < voter_count; i++)
    {
        for (int j = 0; j < candidate_count; j++)
        {
            string name = get_string("Rank %i ", j + 1);

            if (!vote(i, j, name))
            {
                printf("Invalid vote\n");
                j--;
            }
        }
        printf("\n");
    }


    //check_preference();
    while (true)
    {
        tabulate();

        if (print_winner())
        {
            return true;
        }
        else if (is_tie(find_min()))
        {
            return true;
        }
        else
        {
            eliminate(find_min());
        }
    }
}


// Eliminate any candidates in last place
void eliminate(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].eliminated)
        {
            continue;
        }
        else if (min == candidates[i].votes)
        {
            candidates[i].eliminated = true;
        }
    }
}


// Return the minimum number of votes the remaining candidate has
int find_min(void)
{
    int min = MAX;

    for (int i = 1; i < candidate_count; i++)
    {
        if (candidates[i].eliminated)
        {
            continue;
        }
        else if (min > candidates[i].votes)
        {
            min = candidates[i].votes;
        }
    }
    return min;
}


// Returns true if the election is a tie between candidates
bool is_tie(int min)
{
    for (int i = 0; i < candidate_count; i++)
    {
        if (candidates[i].eliminated)
        {
            continue;
        }
        else if (min == candidates[i].votes)
        {
            continue;
        }
        else
        {
            return false;
        }
    }
    return true;
}


// If the vote is valid, then record the ranking preference
bool vote(int voter, int rank, string name)
{
    bool exist = false;

    for (int i = 0; i < candidate_count; i++)
    {
        if (strcmp(name, candidates[preferences[voter][i]].name) == 0 && rank > 0)
        {
            return false;
        }

        if (strcmp(name, candidates[i].name) == 0)
        {
            preferences[voter][rank] = i;
            exist = true;
            break;
        }
    }
    return exist;
}


// Print the winner of the election, if there is one
bool print_winner(void)
{
    float n = (float)voter_count / 2;
    for (int i = 0; i < candidate_count; i++)
    {
        if ((float)candidates[i].votes > n)
        {
            printf("%s\n", candidates[i].name);
            return true;
        }
    }
    return false;
}


// Tabulate the votes for candidates still in race
void tabulate(void)
{
    int check = 0;
    for (int i = 0; i < voter_count; i++)
    {
        if (!candidates[preferences[i][check]].eliminated)
        {
            candidates[preferences[i][check]].votes++;
            check = 0;
        }
        else
        {
            check++;
            i--;
        }
    }
}