
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

def spawn_piece(board):  #unfinished
    # random piece selection (later)
    # random initial rotation (later)

    new_piece = {
        "shape": T,
        "row": 0,
        "col": 4
    }

    return new_piece
    

def can_spawn(board, piece): # unfinished
    # checking whether every occupied cell of piece is currently empty in board
    return True #temp


def get_occupied_cells(piece):

    shape = piece["shape"]  # piece matrix (relative cordinates)
    cells = []

    # iteration on piece to find occupied cells (1's)
    for r in range(len(shape)):
        for c in range(len(shape[r])):
            if shape[r][c] == 1:
                # getting board-relative cords
                board_row = piece["row"] + r
                board_col = piece["col"] + c
                cells.append((board_row, board_col))
    
    return cells


def draw(board, piece):

    temp_board = [row[:] for row in board]

    # getting occupied cells and marking them on temp_board
    for row, col in get_occupied_cells(piece):
        temp_board[row][col] = 1

    # printing temp_board with occupied cells filled
    for row in temp_board:
        for cell in row:
            print("■" if cell!=0 else ".", end="")
        print()


def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")


def can_move(board, piece, direction):
    
    for row, col in get_occupied_cells(piece):

        offset = get_offsets(direction)
        target_row = row + offset[0]
        target_col = col + offset[1]

        # bottom surface
        if target_row >= ROWS:
            return False
        # right surface
        if target_col >= COLS:
            return False
        # left surface
        if target_col < 0:
            return False
        # existing blocks
        if board[target_row][target_col] != 0:
            return False
  
    return True


def get_offsets(direction):
    if direction is "down":
        return 1, 0
    if direction is "right":
        return 0, 1
    if direction is "left":
        return 0, -1


def place_piece(board, piece):
    # getting occupied cells & permenantly marking it on main board
    for row, col in get_occupied_cells(piece):
        board[row][col] = 1


def clear_lines(board):    # unfinished
    pass


def rotate_piece(piece):   # unfinished
    shape = piece["shape"]
    rotated = list(zip(*shape[::-1]))  
    return rotated 


def gameloop():

    tetris = Game()
    tetris.current_piece = spawn_piece(tetris.board)
    game_over = False

    while not game_over:

        # drawing current state
        clear_screen()
        draw(tetris.board, tetris.current_piece)
        # support player moving the piece and re-drawing board before next frame (later)

        # ----- prepration for drawing next state -----
        if can_move(tetris.board, tetris.current_piece, "down"):
            tetris.current_piece["row"] += 1
        else:
            # permenantly place the piece in tetris.baord, then spawn new piece
            place_piece(tetris.board, tetris.current_piece)
            new_piece = spawn_piece(tetris.board)

            if can_spawn(tetris.board, new_piece):
                tetris.current_piece = new_piece
            else:
                # game over if new piece immediately collides with older pieces
                game_over = True
        # ---------------------------------------------

        time.sleep(0.15)

    print(f"GAME OVER ! SCORE: {tetris.score}")


if __name__ == "__main__":
    gameloop()




"""
make some functions use self for cleaner calls

"""