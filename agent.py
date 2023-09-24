from Edge import Edge
from Box import Box 
from board import Board
import os.path
import sys
import time

start = time.time()

minMove = sys.maxsize
maxMove = -sys.maxsize - 1

# Constants
TIME_LIMIT = 10 #currently set at 10 seconds, should be shortened

#global variables
edgeV = []
edgeH = []
board = []
ply = 0
opp = 0
oppMove = [4]
currMove = [4]


class Agent:
    def __init__(self):
        self.t = 0.0
        self.curmove = ""
        self.playername = ""

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
            if edgeH[oppMove[0] +oppMove[1]*10].captured ==False:
                return True
            else:
                print("Move is attempting to capture an edge that has already been claimed")
                return False
        else:
            print("Move is attempting to connect two points that are not adjacent")
            return False

    def check_filler_move(move):
        if move[0] == 0 and move[1] == 0 and move[2] == 0 and move[3] == 0:
            return True
        else:
            return False
          
    # reads the move from move_file.txt and puts the move into oppMove[]      
    def read_move(self):
        file_contents = ''
        with open('move_file.txt', 'r') as file:
            # Read the entire file content into a string
            file_contents = file.read()
        space_index = file_contents.find(' ')
        oppMove[0] = file_contents[space_index+1]
        oppMove[1] = file_contents[space_index+3]
        oppMove[2] = file_contents[space_index+5]
        oppMove[3] = file_contents[space_index+7]

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
        new_move.write(self.playername, " ", currMove[0], ",", currMove[1])
        
    def makeMove (self,):
        bothEdgeList = edgeV + edgeH
        if len(bothEdgeList) < 1:
            #no moves left
            pass
        elif len(bothEdgeList) == 1:
            # 1 move left
            currMove[0] = bothEdgeList[0].x1
            currMove[1] = bothEdgeList[0].y1
            currMove[2] = bothEdgeList[0].x2
            currMove[3] = bothEdgeList[0].y2
            return
        else:
            counter = -1
            sortedList = bothEdgeList.reverse_bubble_sort
            localMin = None
            localMax 
            for itir in sortedList:
                
                counter = counter +1
                tempArray = sortedList
                tempArray.pop(counter)
                for item in range(len(tempArray)):
                    if time.time() - start > TIME_LIMIT -.5:
                        return #best move
                    else: 
                        #calculate evaluation function
                        if item == 0:
                            localmin = tempArray(item).weight
                        elif tempArray(item).weight < localmin:
                            localmin = tempArray(item).weight

                        if localMin <= maxMove:
                            break
                        elif localMin < minMove:
                            minMove = localMin
            
            localMax = localMin
            if(maxMove < localMax):
                maxMove = localMax
            
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
        

def main():
    agent = Agent()
    gameBoard = Board()
    currTime = 0
    startTime = 0
    
    while(gameBoard.check_win is not True):
        #while the move_file.txt file does not exist the program is supposed to wait until it does exist
        while((not os.path.exists("./groupname.go")) or (not os.path.exists("./groupname.pass"))):
            pass

        start = time.time() #timer starts for our player's move

        #read the file, check if it is an empty pass move, check validity, update board, calculate move, write move to file
        agent.read_move()

        if (agent.check_filler_move(oppMove) == True):
            pass #TODO this line should actually make the program spit out an error to the terminal
        else:
            if(agent.check_valid(oppMove) == True):
                agent.update_edge(oppMove, False)
            else:
                pass

        while(time.time() - start < TIME_LIMIT):
            pass #TODO calculate our next move should happen here

        #writes currMove to move_file.txt
        agent.write_move()
    
    #TODO Declare winner:


if __name__ == "__main__":
    main()
