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
    agent = Agent("opps")
    gameBoard = Board()
    agent.board = gameBoard
    end = False
    
    
    print (f'{TEAM_NAME} working')
    while(os.path.exists("move_file")):
        print (f'{TEAM_NAME} main while loop')
        #while the move_file.txt file does not exist the program is supposed to wait until it does exist
        agent.start = time.time()
        while((not os.path.exists(f"{TEAM_NAME}.go")) and (not os.path.exists(f"{TEAM_NAME}.pass"))):
            time.sleep(.1)
            if(time.time()-agent.start>TIME_LIMIT):
                end = True
                break
        if end:
            break
        agent.start = time.time() #timer starts for our player's move

        #read the file, check if it is an empty pass move, check validity, update board, calculate move, write move to file
        agent.read_move()
        if os.path.exists(f"{TEAM_NAME}.pass"):
            agent.board.update_edge(agent.oppMove, False)
            agent.currMove = [0,0,0,0]
            agent.write_move()
        else:
            if(agent.check_filler_move() == True):
                pass
            elif(agent.check_valid() == True):
                print(f'Updating board with {agent.oppMove}')
                agent.board.update_edge(agent.oppMove, False)
            max = agent.makeMove()
            print(max[0])
            agent.board.update_edge(max[1], True)
            
            #writes currMove to move_file.txt
            agent.write_move()
            print(len(agent.board.validEdges))
            
        time.sleep(1)
    
    if (agent.check_win()):
        if(gameBoard.ply - gameBoard.opp > 0):
            print(TEAM_NAME, " has won!")
        else:
            print(agent.opponentName, " has won!")
    

if __name__ == "__main__":
    main()
