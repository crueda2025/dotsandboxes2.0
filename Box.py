from Edge import Edge

class Box:
    def __init__(self, new_top:Edge, new_right:Edge, new_left:Edge, new_bottom:Edge):
        self.top_edge = new_top
        self.right_edge = new_right
        self.left_edge = new_left
        self.bottom_edge = new_bottom
        self.total_edges = 0
        self.captured = False
        self.team = False  # Initialize as False; set to True for ourTeam

    def set_num_edges(self):
        self.total_edges += 1
        # Setting the new box weights in the boxes edges
        self.right_edge.setBTL()
        self.left_edge.setBBR()
        self.bottom_edge.setBBR()
        self.top_edge.setBTL()

    def set_captured(self):
        self.captured = True

    def set_team(self, our_team):
        self.team = our_team