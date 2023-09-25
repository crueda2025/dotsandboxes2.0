from Edge import Edge
from Box import Box 
from board import Board
import os.path
import sys
import time

start = None

# Constants
TIME_LIMIT = 10 #currently set at 10 seconds, should be shortened
TEAM_NAME = "dotsnboxinator"

#global variables
edgeV = []
edgeH = []
board = []
ply = 0
opp = 0
oppMove = []
currMove = []


class Agent:
    def __init__(self):
        self.t = 0.0
        self.curmove = ""
        self.playername = TEAM_NAME
        self.opponentName = ""

    # Return boolean true if valid move
    def check_valid(self, opp_move):
        if (oppMove[0]> 9 or oppMove[0] < 0) or (oppMove[1]> 9 or oppMove[1] < 0) or (oppMove[2]> 9 or oppMove[2] < 0) or (oppMove[3]> 9 or oppMove[3] < 0):
            print("Move is outside the boundaries of the board")
            return False
        elif oppMove[0] == oppMove[2] and 1+oppMove[1] == oppMove[3]:
            if edgeV[oppMove[0] +oppMove[1]*10].captured ==False:
                return True
            else: 
                print("Move is attempting to capture an edge that has already been claimed")
                return False
        elif oppMove[1] == oppMove[3] and 1+oppMove[0] == oppMove[1]:
            if edgeH[oppMove[0] + oppMove[1]*10].captured ==False:
                return True
            else:
                print("Move is attempting to capture an edge that has already been claimed")
                return False
        else:
            print("Move is attempting to connect two points that are not adjacent")
            return False

    def check_filler_move(self, move):
        if move[0] == 0 and move[1] == 0 and move[2] == 0 and move[3] == 0:
            return True
        else:
            return False
          
    # reads the move from move_file.txt and puts the move into oppMove[]      
    def read_move(self):
        file_contents = ''
        tempCoord = []
        tempName = ''
        with open('move_file', 'r') as file:
            # Read the entire file content into a string
            file_contents = file.read()
        temp = file_contents.split(" ")
        if len(temp) < 3:
            print ('We have first move')
            oppMove = [0, 0, 0, 0]
            return
        print(temp)
        tempCoord = temp[1] + ',' + temp[2]
        tempName = temp[0]
        
        #if the name in the move file is our team name, do nothing, if it is not, set the opponent name as the name from the file
        if(tempName == TEAM_NAME):
            pass
        else:
            self.opponentName = tempName
            
        oppMove = []
        
        for m in tempCoord.split(","):
            temp = int(m)
            oppMove.append(temp)

        # checking if the opponent move is in the desired order by the program (ie. "smallest" point first, drawing from left to right or top to bottom)
        if oppMove[0] > oppMove[2]:
            tempx = oppMove[0]
            tempy = oppMove[1]
            oppMove[0] = oppMove [2]
            oppMove[1] = oppMove [3]
            oppMove[2] =  tempx
            oppMove[3] =  tempy
        else:
            if oppMove[1] > oppMove[3]:
                tempx = oppMove[0]
                tempy = oppMove[1]
                oppMove[0] = oppMove [2]
                oppMove[1] = oppMove [3]
                oppMove[2] =  tempx
                oppMove[3] =  tempy

    # overwrites the old move in move_file.txt with the new move
    def write_move(self):
        new_move = open("move_file.txt", "w")
        new_move.write(f"{self.playername} {currMove[0]},{currMove[1]} {currMove[2]}, {currMove[3]}")
    
    def makeMove (self):
        sortedList = board.validEdges.reverse_bubble_sort()
        
        if len(board.bothEdgeList) < 1:
            #no moves left
            pass
        elif len(board.bothEdgeList) == 1:
            # 1 move left
            currMove[0] = board.bothEdgeList[0].x1
            currMove[1] = board.bothEdgeList[0].y1
            currMove[2] = board.bothEdgeList[0].x2
            currMove[3] = board.bothEdgeList[0].y2
            return
        else:
            tempBoard = board
            # Set the first valid move
            maximum  = self.minimax(board, sortedList, 4, True)
            return maximum[1]

                
            
   # returns (hueristic, move)
    # true turn means our team, false means opps team
    def minimax(self, board, validMoves, deep, turn):
        tempArray =  validMoves
        frontArray = []

        if time.time() - start >= TIME_LIMIT-.5:
            return (None, None)
        if turn:
            bestMove = (-sys.maxsize, None)
        else:
            bestMove = (sys.maxsize, None)

        if deep == 0 or len(validMoves) == 0:
            return (board.evalFunc, None)
        for itir in validMoves:
            tempMove = tempArray.pop(0)
            
            #make a duplicate board
            tempBoard = board

            #make a fake move with the duplicate values
            tempPly = tempBoard.ply
            tempOpp = tempBoard.opp
            tempBoard.update_edge(tempMove, turn)
            evalFunc = tempBoard.evalFunc

            
            
            #minimax attempt 1st part
            if turn:
                if evalFunc >= tempBoard.minMove:
                    return (evalFunc, tempMove)
                else:
                    tempBoard.maxMove = evalFunc
            else:
                if evalFunc <= tempBoard.maxMove:
                    return (evalFunc, tempMove)
                else:
                    tempBoard.minMove = evalFunc
            
            #flips the team function 
            if tempPly == tempBoard.ply - 1 or tempOpp == tempBoard - 1:
                turn = not turn

            
            move = self.minimax(tempBoard, frontArray.append(tempArray), deep - 1, not turn)

            if move[0] == None:
                break
            if turn:
                if move[0] > bestMove[0]:
                    bestMove = (move[0], tempMove)
            else:
                if move[0] < bestMove[0]:
                    bestMove = (move[0], tempMove)
            frontArray.append(tempMove)
        return bestMove

            
                    

            
            
    def reverse_bubble_sort(arr:Edge):
        n = len(arr)
        for i in range(n):
            swapped = False

            for j in range(0, n - i - 1):
                # Compare and swap if the element found is less than the next element
                if arr[j].weight < arr[j + 1].weight:
                    arr[j].weight, arr[j + 1].weight = arr[j + 1].weight, arr[j].weight
                    swapped = True

            # If no two elements were swapped in the inner loop, the array is sorted
            if not swapped:
                return
        return    

    #checks for the existence of an end_game.txt file, signifying the end of the game
    def check_win(self):
        if(os.path.exists("end_game.txt")):
            return True
        else:
            return False


def main():
    agent = Agent()
    gameBoard = Board()
    currTime = 0
    startTime = 0
    print ('DotsNBoxinator working')
    while(agent.check_win() == False):
        print ('DotsNBoxinator maine while loop')
        #while the move_file.txt file does not exist the program is supposed to wait until it does exist
        while((not os.path.exists("DotsNBoxinator.go")) and (not os.path.exists("DotsNBoxinator.go.pass"))):
            time.sleep(.1)
            pass

        start = time.time() #timer starts for our player's move

        #read the file, check if it is an empty pass move, check validity, update board, calculate move, write move to file
        agent.read_move()
        
        if(agent.check_filler_move(oppMove) == True):
            pass
        elif(agent.check_valid(oppMove) == True):
            agent.update_edge(oppMove, False)
        agent.makeMove

        #writes currMove to move_file.txt
        agent.write_move()
    
    if (gameBoard.check_win):
        if(gameBoard.ply - gameBoard.opp > 0):
            print(TEAM_NAME, " has won!")
        else:
            print(agent.opponentName, " has won!")


if __name__ == "__main__":
    main()
