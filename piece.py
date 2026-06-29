
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


# SRS kick tables
JLSTZ_KICKS = {
    (0, 1): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    (1, 0): [(0,0), (1,0), (1,-1), (0,2), (1,2)],

    (1, 2): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
    (2, 1): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],

    (2, 3): [(0,0), (1,0), (1,1), (0,-2), (1,-2)],
    (3, 2): [(0,0), (-1,0), (-1,-1), (0,2), (-1,2)],

    (3, 0): [(0,0), (-1,0), (-1,1), (0,-2), (-1,-2)],
    (0, 3): [(0,0), (1,0), (1,-1), (0,2), (1,2)],
}
I_KICKS = {
    (0, 1): [(0,0), (-2,0), (1,0), (-2,-1), (1,2)],
    (1, 0): [(0,0), (2,0), (-1,0), (2,1), (-1,-2)],

    (1, 2): [(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
    (2, 1): [(0,0), (1,0), (-2,0), (1,-2), (-2,1)],

    (2, 3): [(0,0), (2,0), (-1,0), (2,1), (-1,-2)],
    (3, 2): [(0,0), (-2,0), (1,0), (-2,-1), (1,2)],

    (3, 0): [(0,0), (1,0), (-2,0), (1,-2), (-2,1)],
    (0, 3): [(0,0), (-1,0), (2,0), (-1,2), (2,-1)],
}


# ANSI terminal colors
COLORS = {
   -1: "\033[90m",  # light-gray (for ghost piece)
    0: "\033[0m",   # no color (for reseting)
    1: "\033[36m",  # cyan
    2: "\033[33m",  # yellow
    3: "\033[35m",  # pink
    4: "\033[32m",  # green
    5: "\033[31m",  # red
    6: "\033[34m",  # blue
    7: "\033[93m"   # orange

}


PIECES_DATA = {
    "I": {
        "shape": [
            [0,0,0,0],
            [1,1,1,1],
            [0,0,0,0]
        ],
        "color": 1
    },

    "O": {
        "shape": [
            [1,1],
            [1,1]
        ],
        "color": 2
    },

    "T": {
        "shape": [
            [0,0,0,0,0],
            [0,1,1,1,0],
            [0,0,1,0,0],
            [0,0,0,0,0]
        ],
        "color": 3
    },

    "S": {
        "shape": [
            [0,0,0,0,0],
            [0,0,1,1,0],
            [0,1,1,0,0],
            [0,0,0,0,0]
        ],
        "color": 4
    },

    "Z": {
        "shape": [
            [0,0,0,0,0],
            [0,1,1,0,0],
            [0,0,1,1,0],
            [0,0,0,0,0]
        ],
        "color": 5
    },

    "J": {
        "shape": [
            [0,0,0,0],
            [0,0,1,0],
            [0,0,1,0],
            [0,1,1,0],
            [0,0,0,0]
        ],
        "color": 6
    },

    "L": {
        "shape":  [
            [0,0,0,0],
            [0,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,0,0]
        ],
        "color": 7
    }
}