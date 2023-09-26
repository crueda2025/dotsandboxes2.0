from Edge import Edge
from Box import Box 
from board import Board
import os.path
import sys
import time
import copy


# Constants
TIME_LIMIT = 10 #currently set at 10 seconds, should be shortened
TEAM_NAME = "DotsNBoxinator"

#global variables

ply = 0
opp = 0


class Agent:
    def __init__(self, playerName):
        self.t = 0.0
        self.curmove = ""
        self.playername = playerName
        self.opponentName = ""
        self.oppMove = []
        self.currMove = []
        self.board:Board()
        self.start = None

    # Return boolean true if valid move
    def check_valid(self):
        if (self.oppMove[0]> 9 or self.oppMove[0] < 0) or (self.oppMove[1]> 9 or self.oppMove[1] < 0) or (self.oppMove[2]> 9 or self.oppMove[2] < 0) or (self.oppMove[3]> 9 or self.oppMove[3] < 0):
            print("Move is outside the boundaries of the board")
            return False
        elif self.oppMove[0] == self.oppMove[2] and 1+self.oppMove[1] == self.oppMove[3]:
            if self.board.edgeV[self.oppMove[1] +self.oppMove[0]*9].captured ==False:
                return True
            else: 
                print("Move is attempting to capture an edge that has already been claimed")
                return False
        elif self.oppMove[1] == self.oppMove[3] and 1+self.oppMove[0] == self.oppMove[2]:
            if self.board.edgeH[self.oppMove[0] + self.oppMove[1]*9].captured ==False:
                return True
            else:
                print("Move is attempting to capture an edge that has already been claimed")
                return False
        else:
            print(f"Move is attempting to connect two points that are not adjacent {self.oppMove}")
            return False

    def check_filler_move(self):
        if self.oppMove[0] == 0 and self.oppMove[1] == 0 and self.oppMove[2] == 0 and self.oppMove[3] == 0:
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
        if len(temp) <= 1:
            print (f'{self.playername} has first move')
            self.oppMove = [0, 0, 0, 0]
            return
        
        tempCoord = temp[1] + ',' + temp[2]
        tempName = temp[0] 
         
        #if the name in the move file is our team name, do nothing, if it is not, set the opponent name as the name from the file
        if(tempName == TEAM_NAME):
            pass
        else:
            self.opponentName = tempName
            
        self.oppMove = []
        
        for m in tempCoord.split(","):
            temp = int(m)
            self.oppMove.append(temp)

        temprow = self.oppMove[0]
        temprow2 = self.oppMove[2]
        self.oppMove[0] = self.oppMove [1]
        self.oppMove[2] = self.oppMove [3]
        self.oppMove[1] =  temprow
        self.oppMove[3] =  temprow2

        # checking if the opponent move is in the desired order by the program (ie. "smallest" point first, drawing from left to right or top to bottom)
        if self.oppMove[0] > self.oppMove[2]:
            tempx = self.oppMove[0]
            tempy = self.oppMove[1]
            self.oppMove[0] = self.oppMove [2]
            self.oppMove[1] = self.oppMove [3]
            self.oppMove[2] =  tempx
            self.oppMove[3] =  tempy
        else:
            if self.oppMove[1] > self.oppMove[3]:
                tempx = self.oppMove[0]
                tempy = self.oppMove[1]
                self.oppMove[0] = self.oppMove [2]
                self.oppMove[1] = self.oppMove [3]
                self.oppMove[2] =  tempx
                self.oppMove[3] =  tempy
        # flip x and why for row, col vertices
        

    # overwrites the old move in move_file.txt with the new move
    def write_move(self):
        print(f'{TEAM_NAME} WROTE A MOVE')
        print(self.currMove)
        new_move = open("move_file", "w")
        new_move.write(f"{self.playername} {self.currMove[1]},{self.currMove[0]} {self.currMove[3]},{self.currMove[2]}")
    
    def makeMove (self):
        #hold off on bubble sort for right now
        #sortedList = board.validEdges.reverse_bubble_sort()
        validEdges = self.board.validEdges
        if len(validEdges) < 1:
            #no moves left
            pass
        elif len(validEdges) == 1:
            # 1 move left
            self.currMove = []
            self.currMove[0] = validEdges[0].x1
            self.currMove[1] = validEdges[0].y1
            self.currMove[2] = validEdges[0].x2
            self.currMove[3] = validEdges[0].y2
            return self.currMove
        else:
            #self.board.minMove = sys.maxsize
            #self.board.maxMove = -sys.maxsize - 1

            tempBoard = copy.deepcopy(self.board)
            # Set the first valid move
            maximum  = self.minimax(tempBoard, 4, True)
            self.currMove = []
            self.currMove.append(maximum[1][0])
            self.currMove.append(maximum[1][1])
            self.currMove.append(maximum[1][2])
            self.currMove.append(maximum[1][3])

            return maximum

                
            
   # returns (hueristic, move)
    # true turn means our team, false means opps team
    def minimax(self, board, deep, turn):
        tempArray =  copy.deepcopy(board.validEdges)
        frontArray = []

        if time.time() - self.start >= TIME_LIMIT-.5:
            print ('time limit reached returning best move')
            return (None, None)
        
        if turn:
            bestMove = (-sys.maxsize, None)
        else:
            bestMove = (sys.maxsize, None)

        if deep == 0 or tempArray is None:
            return (board.evalFunc, None)
        for itir in tempArray:
            #tempEdge = tempArray.pop(0)

            tempMove = [itir.x1, itir.y1, itir.x2, itir.y2]
            
            #make a duplicate board
            tempBoard = copy.deepcopy(board)

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
                    board.maxMove = evalFunc
                    tempBoard.maxMove = evalFunc
            else:
                if evalFunc <= tempBoard.maxMove:
                    return (evalFunc, tempMove)
                else:
                    board.maxMove = evalFunc
                    tempBoard.minMove = evalFunc
            
            #flips the team function 
            if tempPly == tempBoard.ply - 1 or tempOpp == tempBoard.opp - 1:
                turn = not turn

            
            move = self.minimax(tempBoard, deep - 1, not turn)

            if move[0] == None:
                break
            if turn:
                if move[0] > bestMove[0]:
                    bestMove = (move[0], tempMove)
            else:
                if move[0] < bestMove[0]:
                    bestMove = (move[0], tempMove)
            #frontArray.append(tempMove)
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
        if(os.path.exists("end_game")):
            return True
        else:
            return False


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
            print(f'Updating board with {agent.oppMove}')
            agent.board.update_edge(agent.oppMove, False)
        max = agent.makeMove()
        print(max[0])
        agent.board.update_edge(max[1], True)
        
        #writes currMove to move_file.txt
        agent.write_move()
        #while((not os.path.exists(f"{agent.opponentName}.go")) and (not os.path.exists(f"{agent.opponentName}.pass"))):
        #    time.sleep(.1)
        #    pass
        time.sleep(1)
    
    if (gameBoard.check_win):
        if(gameBoard.ply - gameBoard.opp > 0):
            print(TEAM_NAME, " has won!")
        else:
            print(agent.opponentName, " has won!")
    

if __name__ == "__main__":
    main()
