
class Piece:

    def __init__(self, piece_data, row, col):
        self.shape = piece_data["shape"]
        self.color = piece_data["color"]
        #position on board
        self.row = row
        self.col = col

    
    def get_occupied_cells(self):

        shape = self.shape  # piece matrix (relative cordinates)
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

    
    def rotate(self):  # clockwise
        self.shape = [list(row) for row in zip(*self.shape[::-1])]



PIECES_DATA = {
    "I": {
        "shape": [
            [0,0,0,0],
            [0,0,0,0],
            [1,1,1,1],
            [0,0,0,0],
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
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        "color": 3
    },

    "S": {
        "shape": [
            [0,0,0,0,0],
            [0,0,1,1,0],
            [0,1,1,0,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        "color": 4
    },

    "Z": {
        "shape": [
            [0,0,0,0,0],
            [0,1,1,0,0],
            [0,0,1,1,0],
            [0,0,0,0,0],
            [0,0,0,0,0]
        ],
        "color": 5
    },

    "J": {
        "shape": [
            [0,0,0,0,0],
            [0,0,1,0,0],
            [0,0,1,0,0],
            [0,1,1,0,0],
            [0,0,0,0,0]
        ],
        "color": 6
    },

    "L": {
        "shape":  [
            [0,0,0,0,0],
            [0,1,0,0,0],
            [0,1,0,0,0],
            [0,1,1,0,0],
            [0,0,0,0,0]
        ],
        "color": 7
    }
}