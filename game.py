"""
  ⢠⣾⠿⢷⣄⣀⣠⠤⣤⠢⣤⣾⠏⣤⢹⡇
  ⣼⣿⢸⣶⡝⣿⣿⣷⡘⣧⣸⣿⣾⣿⢸⡧
⢀⣽⣿⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦
⢸⣿⣿⣿⣿⣿⣿⡿⠛⢻⣿⣿⣿⣿⠁⠈⣿⣿⠷⡄  mewlma
⢸⣿⣟⠻⠿⣿⣿⣧⣀⣠⣿⣿⣿⣿⣶⣾⣿⣥⡾⡇
⢸⣿⠿⠿⢶⣾⣿⣿⣿⣿⣿⣿⠟⢻⡿⢻⣿⣿⠶⡇
⢸⣿⣶⣶⣶⠾⣿⣿⣿⣦⣍⣥⣾⣷⣶⣿⣿⣿⣷⠆
⢸⣿⣿⣋⣥⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣏
⢸⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⠈⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉
"""


from piece import Piece
from pieces_data import PIECES_DATA
from srs import JLSTZ_KICKS, I_KICKS
from constants import *
from renderer import Renderer
from input import InputHandler
import time
import random
from colorama import just_fix_windows_console
just_fix_windows_console()


class Game:
    
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = self.spawn_piece()
        self.next_piece = self.spawn_piece()
        self.score = 0
        self.total_lines = 0
        self.level = START_LEVEL
        self.hold_piece = None
        self.can_hold = True   
        self.game_over = False
        self.input = InputHandler()


    def get_fall_interval(self):
        return max(0.03, 0.8 * (0.82 ** (self.level - 1)))
        

    def can_move(self, direction):
        return self.can_move_piece(self.current_piece, direction)


    def can_move_piece(self, piece, direction):
    
        def get_offsets(direction):
            if direction == "down":
                return 1, 0
            if direction == "right":
                return 0, 1
            if direction == "left":
                return 0, -1
            if direction == "neutral":
                return 0, 0
            
        for row, col in piece.get_occupied_cells():

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
            if self.board[target_row][target_col] != 0:
                return False
    
        return True
    

    def place_piece(self):
        # getting occupied cells & permenantly marking it on main board
        for row, col in self.current_piece.get_occupied_cells():
            self.board[row][col] = self.current_piece.color
        
        # checking for lines to clear
        self.clear_lines()


    def clear_lines(self):
        lines_cleared = self.get_completed_rows()
        if lines_cleared:
            self.animate_clearing_lines(lines_cleared)
            self.remove_rows(lines_cleared)
            lines = len(lines_cleared)
            self.score += lines * 100
            self.total_lines += lines
            self.level = START_LEVEL + self.total_lines // LINES_PER_LEVEL

    
    def get_completed_rows(self):

        full_rows = []
        for row in range(ROWS):
            if all(cell != 0 for cell in self.board[row]):
                full_rows.append(row)

        return full_rows
    

    def animate_clearing_lines(self, rows):

        MIDDLE_LEFT = (COLS - 1) // 2
        MIDDLE_RIGHT = COLS // 2

        for offset in range(COLS // 2 + 1):
            for row in rows:

                left = MIDDLE_LEFT - offset
                right = MIDDLE_RIGHT + offset

                if 0 <= left < COLS:
                    self.board[row][left] = 0
                if 0 <= right < COLS:
                    self.board[row][right] = 0

            Renderer.draw(self)
            time.sleep(0.08)


    def remove_rows(self, rows):
        for row in sorted(rows, reverse=True):
            del self.board[row]
        for _ in rows:
            self.board.insert(0, [0] * COLS)


    def spawn_piece(self):

        # selecting a random piece and creating it
        piece_type = random.choice(list(PIECES_DATA.keys()))
        new_piece = Piece(piece_type, 0, 4)

        # selecting a random number of rotations
        random_initial_rotation = random.randint(0,3)
        for _ in range(random_initial_rotation):
            new_piece.rotate('cw')

        # removing top paddings (zeros in shape matrice)
        new_piece.row = -new_piece.get_top_padding()

        return new_piece
    

    def can_spawn(self, piece):

        # checking whether any occupied cell of spawning-piece is empty in board
        for row, col in piece.get_occupied_cells():
            # checking for bad pieces
            assert 0 <= row < ROWS
            assert 0 <= col < COLS
            # collides with existing block
            if self.board[row][col] != 0:
                return False

        return True
    

    def gravity(self):

        if self.can_move("down"):
            self.current_piece.row += 1
        else:
            self.lock_and_spawn()


    def hard_drop(self):
        while self.can_move("down"):
            self.current_piece.row += 1
        self.lock_and_spawn()


    def lock_and_spawn(self):
        self.place_piece()
        self.current_piece = self.next_piece
        self.next_piece = self.spawn_piece()
        self.can_hold = True
        if not self.can_spawn(self.current_piece):
            self.game_over = True
            

    def get_ghost(self):

        ghost = Piece(self.current_piece.type, self.current_piece.row, self.current_piece.col)
        ghost.rotation = self.current_piece.rotation

        while self.can_move_piece(ghost, "down"):
            ghost.row += 1

        return ghost
    

    def hold(self):

        if not self.can_hold:
            return
        else:
            self.can_hold = False

        if self.hold_piece is None:
            self.hold_piece = self.current_piece
            self.current_piece = self.next_piece
            self.next_piece = self.spawn_piece()
            self.current_piece.reset_position()
        else:
            self.current_piece, self.hold_piece = self.hold_piece, self.current_piece
            self.current_piece.reset_position()

        if not self.can_spawn(self.current_piece):
            self.game_over = True
    

    def try_rotate(self, direction):

        piece = self.current_piece
        old_rotation = piece.rotation
        old_row = piece.row
        old_col = piece.col

        # compute new rotation
        if direction == "cw":
            new_rotation = (old_rotation + 1) % 4
        else:
            new_rotation = (old_rotation - 1) % 4

        # select kick table
        if piece.type == "I":
            kicks = I_KICKS.get((old_rotation, new_rotation), [(0,0)])
        elif piece.type == "O":
            kicks = [(0,0)]
        else:
            kicks = JLSTZ_KICKS.get((old_rotation, new_rotation), [(0,0)])

        # try each kick
        for dx, dy in kicks:

            piece.rotation = new_rotation
            piece.row = old_row + dy
            piece.col = old_col + dx

            if self.can_move("neutral"):
                return True

        # revert if failed
        piece.rotation = old_rotation
        piece.row = old_row
        piece.col = old_col
        return False
                


def gameloop():

    tetris = Game()
    Renderer.initialize_screen()
    last_fall_time = time.time()  

    while not tetris.game_over:

        # drawing current state
        Renderer.draw(tetris)

        # keyboard input
        tetris.input.update(tetris)

        # skipping gravity, if fall interval is not completed yet
        # for updating rotation/movement before next
        current_time = time.time()
        if current_time - last_fall_time >= tetris.get_fall_interval():
            tetris.gravity()
            last_fall_time = current_time

        time.sleep(0.01)

    # show final spawning collision and GAMEOVER
    Renderer.draw(tetris)
    print("GAME OVER!")


if __name__ == "__main__":
    gameloop()




"""
TO DO:

refactor
make README + req.txt
game version releases in github
cross platform

7 bag randomizer (is it really?)
lockdown delay
pause
better terminal (high score, level, time)
themes

gui?
port

"""