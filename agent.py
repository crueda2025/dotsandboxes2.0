from Edge import Edge
import Box 
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
        elif oppMove[1] == oppMove[3] and 1+oppMove[0] == oppMove[1]:
            if edgeH[oppMove[0] +oppMove[1]*10].captured ==False:
                return True
        else:
            print("Move is attempting to capture an edge that has already been claimed")
            return False
        pass

    def check_filler_move(move):
        if move[0] == 0 and move[1] == 0 and move[2] == 0 and move[3] == 0:
            return True
        else:
            return False

    def update_edge(self, move, team):
        # Vertical
        if move[0] == move[2] and 1 + move[1] == move[3]:
            #update in the vertical edge array
            edgeV[move[0] + move[1]* 9].setCaptured()

            if(move[0] == 0):#edge case of left side
                # update the value of the box on the right 
                board[move[0] + move[1] * 8].setNumEdges()
                if board[move[0] + move[1] * 8].totalEdges == 4:
                    board[move[0] + move[1] * 8].setCaptured()
                    board[move[0] + move[1] * 8].setTeam(team)
                    if team:
                        ply+=1
                    else:
                        opp+=1
            elif move[0] == 9:#edge case of the right side
            #update the value of the box on the left
                board[move[0] + move[1] * 8 - 1].setNumEdges()
                if board[move[0] + move[1] * 8 - 1].totalEdges == 4:
                    board[move[0] + move[1] * 8 - 1].setCaptured()
                    board[move[0] + move[1] * 8 - 1].setTeam(team)
                    if team:
                        ply+=1
                    else:
                        opp+=1
            else:
                # update the value of the box on the right
                board[move[0] + move[1] * 8].setNumEdges()
                #check if captured
                if board[move[0] + move[1] * 8].totalEdges == 4:
                    board[move[0] + move[1] * 8].setCaptured()
                    board[move[0] + move[1] * 8].setTeam(team)
                    if team:
                        ply+=1
                    else:
                        opp+=1
                # update the value of the box on the left
                board[move[0] + move[1] * 8 - 1].setNumEdges()
                #check if captured
                if board[move[0] + move[1] * 8 - 1].totalEdges == 4:
                    board[move[0] + move[1] * 8 - 1].setCaptured()
                    board[move[0] + move[1] * 8 - 1].setTeam(team)
                    if team:
                        ply+=1
                    else:
                        opp+=1
        # Horizontal        
        elif move[1] == move[3] and move[0] == 1 + move[2]:
            edgeH[move[0] + move[1]* 10].setCaptured()
            #updates amount of edges box has
            if move[1] == 0:
                board[move[0] + move[1] * 8].setNumEdges()
                #if box on the bottom was captured
                if board[move[0] + move[1] * 8].totalEdges == 4:
                    board[move[0] + move[1] * 8].setCaptured()
                    board[move[0] + move[1] * 8].setTeam(team)
                    if team:
                        ply+=1
                    else:
                        opp+=1
            elif move[1] == 9:
                board[move[0] + move[1] * 8 - 1].setNumEdges()
                #//if box on the top was captured
                if(board[move[0] + move[1] * 8 - 1].totalEdges == 4):
                    board[move[0] + move[1] * 8 - 1].setCaptured()
                    board[move[0] + move[1] * 8 - 1].setTeam(team)
                    if team:
                        ply+=1
                    else:
                        opp+=1
            else:
                board[move[0] + move[1] * 8].setNumEdges()
                #//if box on the bottom was captured
                if board[move[0] + move[1] * 8].totalEdges == 4:
                    board[move[0] + move[1] * 8].setCaptured()
                    board[move[0] + move[1] * 8].setTeam(team)
                    if team:
                        ply+=1
                    else:
                        opp+=1
                board[move[0] + move[1] * 8 - 1].setNumEdges(board[move[0] + move[1] * 8- 1].totalEdges + 1)
                #//if box on the top was captured
                if board[move[0] + move[1] * 8 - 1].totalEdges == 4:
                    board[move[0] + move[1] * 8 - 1].setCaptured()
                    board[move[0] + move[1] * 8 - 1].setTeam(team)
                    if team:
                        ply+=1
                    else:
                        opp+=1
                  
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

    def check_win(self):
        # Your check win logic here
        if ply + opp == 81:
            return True
        else:
            return False
        
    def makeMove (self):
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
    currTime = 0
    startTime = 0

    edgeV = [Edge(0, 0, 0, 0) for _ in range(90)]
    edgeH = [Edge(0, 0, 0, 0) for _ in range(90)]
    board = [Box(Edge(0, 0, 0, 0), Edge(0, 0, 0, 0), Edge(0, 0, 0, 0), Edge(0, 0, 0, 0)) for _ in range(81)]

    for y in range(9):
        for x in range(10):
            edgeV[x + y * 10] = Edge(x, y, x, y + 1)

    for y in range(10):
        for x in range(9):
            edgeH[x + y * 9] = Edge(x, y, x + 1, y)

    for y in range(9):
        for x in range(9):
            board[x + y * 8] = Box(edgeH[x + y * 8], edgeV[x + y * 8 + 1], edgeV[x + y * 8], edgeH[x + y * 8 + 1])
    
    while(agent.check_win is not True):
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

        #TODO write the new move to move_file.txt
    
    #TODO Declare winner:


if __name__ == "__main__":
    main()
