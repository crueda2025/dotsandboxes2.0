from Edge import Edge
from Box import Box 
from board import Board
from agent import Agent
import os.path
import time
import copy



# Constants
TIME_LIMIT = 10 #currently set at 10 seconds, should be shortened
TEAM_NAME = "opps"

#global variables

ply = 0
opp = 0

def main():
    agent = Agent(TEAM_NAME)
    gameBoard = Board()
    agent.board = gameBoard
    
    print (f'{TEAM_NAME} working')
    while(agent.check_win() == False):
        print (f'{TEAM_NAME} main while loop')
        #while the move_file.txt file does not exist the program is supposed to wait until it does exist
        while((not os.path.exists(f"{TEAM_NAME}.go")) and (not os.path.exists(f"{TEAM_NAME}.pass"))):
            time.sleep(.1)
            pass

        agent.start = time.time() #timer starts for our player's move

        #read the file, check if it is an empty pass move, check validity, update board, calculate move, write move to file
        agent.read_move()
        
        if(agent.check_filler_move() == True):
            pass
        elif(agent.check_valid() == True):
            print('Updating board with opp move')
            agent.board.update_edge(agent.oppMove, False)
        agent.board.update_edge(agent.makeMove(), True)
        
        #writes currMove to move_file.txt
        agent.write_move()
        while((not os.path.exists(f"{agent.opponentName}.go")) and (not os.path.exists(f"{agent.opponentName}.pass"))):
            time.sleep(.1)
            pass
    
    if (gameBoard.check_win):
        if(gameBoard.ply - gameBoard.opp > 0):
            print(TEAM_NAME, " has won!")
        else:
            print(agent.opponentName, " has won!")
    

if __name__ == "__main__":
    main()
