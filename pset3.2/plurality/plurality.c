#include <cs50.h>
#include <stdio.h>
#include <string.h>

// Max number of candidates
#define MAX 9

// Candidates have name and vote count
typedef struct
{
    string name;
    int votes;
}
candidate;

// Array of candidates
candidate candidates[MAX];

// Number of candidates
int candidate_count;

// Function prototypes
bool vote(string name);
void print_winner(void);

int main(int argc, string argv[])
{
    // Check for invalid usage
    if (argc < 2)
    {
        printf("Usage: plurality [candidate ...]\n");
        return 1;
    }

    // Populate array of candidates
    candidate_count = argc - 1;
    if (candidate_count > MAX)
    {
        printf("Maximum number of candidates is %i\n", MAX);
        return 2;
    }
    for (int i = 0; i < candidate_count; i++)
    {
        candidates[i].name = argv[i + 1];
        candidates[i].votes = 0;
    }

    int voter_count = get_int("Number of voters: ");

    // Loop over all voters
    for (int i = 0; i < voter_count; i++)
    {
        string name = get_string("Vote: ");

        // Check for invalid vote
        if (!vote(name))
        {
            printf("Invalid vote.\n");
        }
    }

    // Display winner of election
    print_winner();
}

// Update vote totals given a new vote
bool vote(string name)
{
    // Assume candidate does not exist
    bool exist = false;

    for (int i = 0; i < candidate_count; i++)
    {
        //check if the user entered name is in the list of candidates
        if (strcmp(name, candidates[i].name) == 0)
        {
            // Add a vote for that candidate
            candidates[i].votes++;
            // Candidate exists
            exist = true;
            break;
        }
    }
    return exist;
}


// Print the winner (or winners) of the election
void print_winner(void)
{
    // Create a variable to keep track of candidate votes
    int maxVote = 0;

    // Iterate over array of candidates
    for (int i = 0; i < candidate_count; i++)
    {
        // Check if candidate has more than the current max votes
        if (candidates[i].votes > maxVote)
        {
            // Change maxVotes to that candidate's number of votes
            maxVote = candidates[i].votes;
        }
    }
    // Iterate over array of candidates
    for (int j = 0; j < candidate_count; j++)
    {
        // If the candiate has the max number of votes then print that candidate as the winner
        if (candidates[j].votes == maxVote)
        {
            printf("%s\n", candidates[j].name);
        }
    }
}
