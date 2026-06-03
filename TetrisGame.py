
import time
import os

COLS = 10
ROWS = 20

class Game:
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = 2
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


def draw(board, piece):

    temp_board = [row[:] for row in board]

    # manualy inserting piece (for now)
    shape = piece["shape"]
    row_pos = piece["row"]
    col_pos = piece["col"]

    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] == 1:
                temp_board[row_pos + r][col_pos + c] = 1

    for row in temp_board:
        for cell in row:
            print("#" if cell else ".", end="")
        print()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


# def can_move(piece, new_row, new_col):
#     # Left wall
#     if new_col < 0:
#         # Right wall
#         if new_col + piece_width > COLS:
#             # Bottom
#             if new_row + piece_height > ROWS:
#                 # Existing blocks
#                 if board[row][col] != 0:
#                     return True
#     return False

def spawn_piece():  
    # random piece selection later
    return {
        "shape": T,
        "row": 0,
        "col": 4
    }


def gameloop():

    tetris = Game()
    tetris.current_piece = spawn_piece()

    while True:
        clear_screen()
        draw(tetris.board, tetris.current_piece)
        tetris.current_piece["row"] += 1
        time.sleep(0.5)


if __name__ == "__main__":
    gameloop()