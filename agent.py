from Edge import Edge
import Box 
import time
import os.path

# Constants
TIME_LIMIT = 10 #currently set at 10 seconds, should be shortened

#global variables
edgeV = [90]
edgeH = [90]
board = [81]
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
            return False
        elif oppMove[0] == oppMove[2] and 1+oppMove[1] == oppMove[3]:
            if edgeV[oppMove[0] +oppMove[1]*10].captured ==False:
                return True
        elif oppMove[1] == oppMove[3] and 1+oppMove[0] == oppMove[1]:
            if edgeH[oppMove[0] +oppMove[1]*10].captured ==False:
                return True
        else:
            return False
        pass

    def check_filler_move(move):
        if move[0] == 0 and move[1] == 0 and move[2] == 0 and move[3] == 0:
            return True
        else:
            return False


    def update_edge(self, opp_move):
        # Your update edge logic here
        if oppMove[0] == oppMove[2] and 1 + oppMove[1] == oppMove[3]:
            #update in the vertical edge array
            edgeV[oppMove[0] + oppMove[1]* 9].setCaptured()

            if(oppMove[0] == 0):#edge case of left side
                # update the value of the box on the right 
                board[oppMove[0] + oppMove[1] * 8].setNumEdges()
                if board[oppMove[0] + oppMove[1] * 8].totalEdges == 4:
                    board[oppMove[0] + oppMove[1] * 8].setCaptured()
                    board[oppMove[0] + oppMove[1] * 8].setTeam(False)
                    opp+=1
            elif oppMove[0] == 9:#edge case of the right side
            #update the value of the box on the left
                board[oppMove[0] + oppMove[1] * 8 - 1].setNumEdges()
                if board[oppMove[0] + oppMove[1] * 8 - 1].totalEdges == 4:
                    board[oppMove[0] + oppMove[1] * 8 - 1].setCaptured()
                    board[oppMove[0] + oppMove[1] * 8 - 1].setTeam(False)
                    opp+=1
            else:
                # update the value of the box on the right
                board[oppMove[0] + oppMove[1] * 8].setNumEdges()
                #check if captured
                if board[oppMove[0] + oppMove[1] * 8].totalEdges == 4:
                    board[oppMove[0] + oppMove[1] * 8].setCaptured()
                    board[oppMove[0] + oppMove[1] * 8].setTeam(False)
                    opp+=1
                # update the value of the box on the left
                board[oppMove[0] + oppMove[1] * 8 - 1].setNumEdges()
                #check if captured
                if board[oppMove[0] + oppMove[1] * 8 - 1].totalEdges == 4:
                    board[oppMove[0] + oppMove[1] * 8 - 1].setCaptured()
                    board[oppMove[0] + oppMove[1] * 8 - 1].setTeam(False)
                    opp+=1
        # Horizontal        
        elif oppMove[1] == oppMove[3] and oppMove[0] == 1 + oppMove[2]:
            edgeH[oppMove[0] + oppMove[1]* 10].setCaptured()
            #updates amount of edges box has
            if oppMove[1] == 0:
                board[oppMove[0] + oppMove[1] * 8].setNumEdges()
                #if box on the bottom was captured
                if board[oppMove[0] + oppMove[1] * 8].totalEdges == 4:
                        board[oppMove[0] + oppMove[1] * 8].setCaptured()
                        board[oppMove[0] + oppMove[1] * 8].setTeam(False)
                        opp+1
            elif oppMove[1] == 9:
                board[oppMove[0] + oppMove[1] * 8 - 1].setNumEdges()
                #//if box on the top was captured
                if(board[oppMove[0] + oppMove[1] * 8 - 1].totalEdges == 4):
                    board[oppMove[0] + oppMove[1] * 8 - 1].setCaptured()
                    board[oppMove[0] + oppMove[1] * 8 - 1].setTeam(False)
                    opp+1
            else:
                board[oppMove[0] + oppMove[1] * 8].setNumEdges()
                #//if box on the bottom was captured
                if board[oppMove[0] + oppMove[1] * 8].totalEdges == 4:
                    board[oppMove[0] + oppMove[1] * 8].setCaptured()
                    board[oppMove[0] + oppMove[1] * 8].setTeam(False)
                    opp+1
                board[oppMove[0] + oppMove[1] * 8 - 1].setNumEdges(board[oppMove[0] + oppMove[1] * 8- 1].totalEdges + 1);
                #//if box on the top was captured
                if board[oppMove[0] + oppMove[1] * 8 - 1].totalEdges == 4:
                    board[oppMove[0] + oppMove[1] * 8 - 1].setCaptured()
                    board[oppMove[0] + oppMove[1] * 8 - 1].setTeam(False)
                    opp+1
                  
                          

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
    
    #while the move_file.txt file does not exist the program is supposed to wait until it does exist
    while(not (os.path.exists("./move_file.txt"))):
        pass

    start = time.time() #timer starts for our player's move

    #read the file, check if it is an empty pass move, check validity, update board, calculate move, write move to file
    read_move()

    if (check_filler_move(oppMove) == True):
        pass #TODO this line should actually make the program spit out an error to the terminal
    else:
        if(check_valid(oppMove) == True):
            update_edge(oppMove)
        else:
            pass #TODO this line should also spit out an error to the terminal

    while(time.time() - start < TIME_LIMIT):
        pass #TODO calculate our next move should happen here

    #TODO write the new move to move_file.txt


if __name__ == "__main__":
    main()
