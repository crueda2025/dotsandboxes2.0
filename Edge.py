class Edge:
    def __init__(self, x1C, y1C, x2C, y2C):
        self.captured = False
        self.weight = 1
        self.bTL = 0
        self.bBR = 0
        self.chainWeight = 1
        self.x1 = x1C
        self.y1 = y1C
        self.x2 = x2C
        self.y2 = y2C

    def setBTL(self, newBTL):
        self.bTL = newBTL

    def setBBR(self, newBBR):
        self.bBR = newBBR

    def setCaptured(self):
        self.captured = True

    def setWeight(self):
        # TODO: Implement this method
        if self.bBR == 1 and self.bTL == 1:
            self.weight = 2
        elif self.bBR == 3 or self.bTL == 3:
            self.weight = self.chainWeight * 3
        elif self.bBR == 2 or self.bTL == 2:
            self.weight = self.chainWeight * -1
        elif self.bBR == 1 or self.bTL == 1:
            self.weight = 1
        

        