
import time
import os

COLS = 10
ROWS = 20

class Game:
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = None
        self.score = 0

I = [
    [1],
    [1],
    [1],
    [1]
]

O = [
    [1, 1],
    [1, 1]
]

T = [
    [1, 1, 1],
    [0, 1, 0]
]

S = [
    [0, 1, 1],
    [1, 1, 0]
]

Z = [
    [1, 1, 0],
    [0, 1, 1]
]

J = [
    [0, 1],
    [0, 1],
    [1, 1]
]

L = [
    [1, 0],
    [1, 0],
    [1, 1]
]

PIECES = [I, O, T, S, Z, J, L]

def spawn_piece():  
    # random piece selection (later)
    # random initial rotation (later)
    piece = 'T'
    if piece == 'T':
        return {
            "shape": T,
            "row": 0,
            "col": 4
        }


def draw(board, piece):

    temp_board = [row[:] for row in board]

    shape = piece["shape"]  # piece matrix (relative cordinates)
    row_pos = piece["row"]
    col_pos = piece["col"]

    # iteration on piece to find occupied cells (1's)
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] == 1:
                # marking occupation on temp_board
                temp_board[row_pos + r][col_pos + c] = 1

    # printing board with occupied cells filled
    for row in temp_board:
        for cell in row:
            print("■" if cell!=0 else ".", end="")
        print()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def can_move_down(board, piece):

    shape = piece["shape"]

    # iteration on piece to find occupied cells (1's)
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] == 1:
                # converting piece-relative coordinates to board-coordinates 
                board_row = piece["row"] + r
                board_col = piece["col"] + c

                # the cell underneath
                target_row = board_row + 1
                target_col = board_col 

                # bottom surface
                if target_row >= ROWS:
                    return False
                # existing blocks
                if board[target_row][target_col] != 0:
                    return False   
    return True       


def place_piece(board, piece):
    
    shape = piece["shape"]

    # iteration on piece to find occupied cells
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] == 1:
                # permenantly marking it on main board
                board_row = piece["row"] + r
                board_col = piece["col"] + c
                board[board_row][board_col] = 1


def gameloop():

    tetris = Game()
    tetris.current_piece = spawn_piece()

    while True:
        # drawing current state
        clear_screen()
        draw(tetris.board, tetris.current_piece)
        # support player moving the piece and re-drawing board before next frame (later)

        # ----- prepration for drawing next state -----

        if can_move_down(tetris.board, tetris.current_piece):
            tetris.current_piece["row"] += 1
        else:
            # permenantly place the piece in tetris.baord
            place_piece(tetris.board, tetris.current_piece)
            # spawn new piece
            tetris.current_piece = spawn_piece()

        # ---------------------------------------------

        time.sleep(0.15)


if __name__ == "__main__":
    gameloop()