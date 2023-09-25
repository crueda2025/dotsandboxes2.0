from Box import *
import sys
class Board:
    def __init__(self):
        self.edgeV = [Edge(0, 0, 0, 0) for _ in range(90)]
        self.edgeH = [Edge(0, 0, 0, 0) for _ in range(90)]
        self.board = [Box(Edge(0, 0, 0, 0), Edge(0, 0, 0, 0), Edge(0, 0, 0, 0), Edge(0, 0, 0, 0)) for _ in range(81)]

        for y in range(9):
            for x in range(10):
                self.edgeV[x + y * 10] = Edge(x, y, x, y + 1)

        for y in range(10):
            for x in range(9):
                self.edgeH[x + y * 9] = Edge(x, y, x + 1, y)

        for y in range(9):
            for x in range(9):
                self.board[x + y * 8] = Box(self.edgeH[x + y * 8], self.edgeV[x + y * 8 + 1], self.edgeV[x + y * 8], self.edgeH[x + y * 8 + 1])
        self.ply = 0
        self.opp = 0
        self.evalFunc = 0
        
        self.validEdges = self.edgeV
        self.validEdges.append(self.edgeH)
        self.minMove = sys.maxsize
        self.maxMove = -sys.maxsize - 1

    def evaluate(self):
        self.evalFunc = self.ply - self.opp

    #maybe add an array of all uncaptured edges
    # Checks if captured, if so sets team and adds score
    def check_cap(self, num, team):
        if self.board[num].totalEdges == 4:
            self.board[num].setCaptured()
            self.board[num].setTeam(team)
            if team:
                self.ply+=1
            else:
                self.opp+=1
            self.evaluate()
            

    #team is true if our team, false if the opponent
    # Returns the heuristic weight of the edge
    def update_edge(self, move, team):
        hueristic = None
        # Vertical
        if move[0] == move[2] and 1 + move[1] == move[3]:
            #update in the vertical edge array
            self.edgeV[move[0] + move[1]* 9].setCaptured()
            hueristic = self.edgeV[move[0] + move[1]* 9].weight

            if(move[0] == 0):#edge case of left side
                # update the value of the box on the right 
                self.board[move[0] + move[1] * 8].setNumEdges()
                self.check_cap(move[0] + move[1] * 8, team)
            elif move[0] == 9:#edge case of the right side
            #update the value of the box on the left
                self.board[move[0] + move[1] * 8 - 1].setNumEdges()
                self.check_cap(move[0] + move[1] * 8 - 1, team)
            else:
                # update the value of the box on the right
                self.board[move[0] + move[1] * 8].setNumEdges()
                #check if captured
                self.check_cap(move[0] + move[1] * 8, team)
                # update the value of the box on the left
                self.board[move[0] + move[1] * 8 - 1].setNumEdges()
                #check if captured
                self.check_cap(move[0] + move[1] * 8 - 1, team)
        # Horizontal        
        elif move[1] == move[3] and move[0] == 1 + move[2]:
            self.edgeH[move[0] + move[1]* 10].setCaptured()
            hueristic = self.edgeH[move[0] + move[1]* 10].weight
            #updates amount of edges box has
            if move[1] == 0:
                self.board[move[0] + move[1] * 8].setNumEdges()
                #if box on the bottom was captured
                self.check_cap(move[0] + move[1] * 8, team)

            elif move[1] == 9:
                self.board[move[0] + move[1] * 8 - 1].setNumEdges()
                #//if box on the top was captured
                self.check_cap(move[0] + move[1] * 8 - 1, team)

            else:
                # set edges in first box
                self.board[move[0] + move[1] * 8].setNumEdges()
                #//if box on the bottom was captured
                self.check_cap(move[0] + move[1] * 8, team)
                
                # set edges in second box
                self.board[move[0] + move[1] * 8 - 1].setNumEdges(self.board[move[0] + move[1] * 8- 1].totalEdges + 1)
                
                #//if box on the top was captured
                self.check_cap(move[0] + move[1] * 8 - 1, team)
        
        #for all the valid edges remaining, check to see if they were marked as captured
        #if marked as captured, remove them from the list of valid moves/edges remaining
        for each in self.validEdges:
            if each.captured:
                self.validEdges.remove(each)
        return hueristic

