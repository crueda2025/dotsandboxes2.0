

class Box:
    def __init__(self, new_top, new_right, new_left, new_bottom):
        self.top_edge = new_top
        self.right_edge = new_right
        self.left_edge = new_left
        self.bottom_edge = new_bottom
        self.total_edges = 0
        self.captured = False
        self.team = False  # Initialize as False; set to True for ourTeam

    def set_num_edges(self, edges_captured):
        self.total_edges = edges_captured

    def set_captured(self):
        self.captured = True

    def set_team(self, our_team):
        self.team = our_team