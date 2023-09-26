# dotsandboxes2.0
## Work Distribution

## User Instructions
1. Run the agent.py file, it contains the main() method for the program
2. Inside the agent.py file it contains several constants:
    - TIME_LIMIT controls the amount of time the program is allowed to use to calculate a new move
    - TEAM_NAME the name of the program's team

## Utility Function
    The utility function is kept very simple by calculating the difference between the number of boxes our agent has captured and the number of boxes the opponent's agent has captured. This keeps accurate to the terminal nodes because the win/loss/draw conditions are determined by the number of boxex captured. The utility function falls under the Board class, as the board is the object that keeps track of how many boxes each team has captured. 

## Evaluation Function
    The evaluation function is virtually the same as the utility function. This allows for the evaluation function to remain equivalent to the utility function's evaluation of the terminal nodes. In the beginning of the games this does mean that the evaluation function doesn't play as heavy as a role in deciding what move to pick, and instead that work is mostly directed by the heuristic. We decided that in the early game as the initial move you make doesn't matter as much on a larger board like the one we're using this was alright.

## Heuristic
    The heuristic incorporates some knowledge we acquired from studying the game theory behind dots and boxes. It places more weight on edges based on the two boxes adjacent to it. For example, a horizontal line is touching the box above it and the box below it. The heuristic takes into account how many edges on those adjacent boxes have been captured. For an edge that is adjacent to a box that already has two edges captured, it is weighted negatively, as the edge being considered would create a box with three sides captured, giving the opponent agent an opportunity to capture that box. The edges weighted highest are ones that already have three sides captured, as that edge we are considering would allow us to complete and capture a box. Boxes with only one edge captured are second highest, as they allow for the formation of "chains" or multiple boxes in a row that can possibly be captured one after the other if you play your cards right. Boxes that have two edges each adjacent to the edge in question are not desirable because it will create an opportunity for the opponent to score.

    Priority in edges that interest us:
    1. An edge that has an adjacent box with three edges already captured, allowing for our agent to capture a box
    2. An edge that has two adjacent boxes with only one edge already captured, allowing for our agent to create "chains" of boxes
    3. An edge that has an adjacent box with no edges captured
    4. An edge that has two adjacent boxes with two edges captured, this creates a scenario where we "give away" boxes to our opponent.

## Results
    Our initial tests were run against human players. This allowed us to give the agent specific cases, whether they were edge cases or specific behavior we wanted to encourage, as the human player could specify certain moves to validate the agent's ability at recognizing valid/invalid moves.

    After testing against human players we made our program play itself

- describe which tests you ran to try out your program
- did the program play against human players?
- did the program play against itself?
- did the program play against other programs?
- how did the program do during these games?
- describe the strengths and weaknesses of the program

## Discussion
    The evaluation function we chose is good because it is simple and remains consistent with the utility function no matter what. It does have some limitations at the beginning of the game because it doesn't provide as much "guidance" as it does after the board begins to fill up. 

    The heuristic we chose is good because it takes into account the surroundings of the edge in question. In smaller boards this becomes more imperative, but our heuristic allows for the agent to take into account the possibility of "chaining" boxes together. By restricting/weighting moves that have an adjacent box with two edges already captured we can avoid giving away boxes to our opponent to capture. By evaluating the adjacent boxes to an edge

- why are the evaluation and function and heuristic(s) you chose good?