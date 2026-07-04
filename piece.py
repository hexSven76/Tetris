
from pieces_data import PIECES_DATA

class Piece:

    def __init__(self, piece_type, row, col):
        self.type = piece_type
        self.color = PIECES_DATA[piece_type]["color"]
        self.rotation = 0   # 0=spawn | 1=right | 2=180 | 3=left
        #position on board
        self.row = row
        self.col = col


    def get_shape(self):
        shape = PIECES_DATA[self.type]["shape"]
        for _ in range(self.rotation):
            shape = [list(row) for row in zip(*shape[::-1])]
        return shape

    
    def get_occupied_cells(self):

        shape = self.get_shape()  # piece matrix (relative cordinates)
        cells = []    

        # iteration on piece to find occupied cells (1's)
        for r in range(len(shape)):
            for c in range(len(shape[r])):
                if shape[r][c] == 1:
                    # getting board-relative cords
                    board_row = self.row + r
                    board_col = self.col + c
                    cells.append((board_row, board_col))

        return cells

    
    def rotate(self, direction):
        if direction == "cw":
            self.rotation = (self.rotation + 1) % 4
        elif direction == "ccw":
            self.rotation = (self.rotation - 1) % 4


    def get_top_padding(self):
        for r, row in enumerate(self.get_shape()):
            if any(cell == 1 for cell in row):
                return r
        return 0
    

    def reset_position(self):  # used when swapping to hold piece
        self.row = -self.get_top_padding()
        self.col = 4
        