from Edge import *
from Box import *

class Board:
    def __init__(self):
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
        self.ply = 0
        self.opp = 0
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
            

        