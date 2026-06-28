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

import time
import random
import msvcrt
import sys
from piece import Piece, PIECES_DATA, COLORS, WALL_KICKS
from colorama import just_fix_windows_console
just_fix_windows_console()

COLS = 10
ROWS = 20
START_LEVEL = 8
LINES_PER_LEVEL = 10

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


    def get_fall_interval(self):
        return max(0.03, 0.8 * (0.82 ** (self.level - 1)))
    

    def initialize_screen(self):
        sys.stdout.write("\033[?1049h")  # switch to alternate buffer
        sys.stdout.write("\033[?25l") # hide cursor
        sys.stdout.flush()


    def draw(self):

        # concating everything in one string to print it once
        frame = "\033[H\033[0J"
        temp_board = [row[:] for row in self.board]

        # getting ghost piece and marking it on temp_board
        ghost = self.get_ghost()
        for row, col in ghost.get_occupied_cells():
            if 0 <= row < ROWS and 0 <= col < COLS:
                temp_board[row][col] = -1

        # getting occupied cells and marking them on temp_board
        for row, col in self.current_piece.get_occupied_cells():
            temp_board[row][col] = self.current_piece.color

        # top border
        frame += "┌" + "─" * (COLS * 2) + "┐\n"

        # printing temp_board with occupied cells filled
        for row in temp_board:
            printing_line = ""
            for cell in row:
                if cell == 0:
                    printing_line += "  "
                elif cell == -1:
                    printing_line += COLORS[-1] + "░░" + COLORS[0]
                else:
                    printing_line += COLORS[cell] + "██" + COLORS[0]

            # side borders
            frame += "│" + printing_line + "│\n"

        # lower border  
        frame += "└" + "─" * (COLS * 2) + "┘\n"
        frame += f"\nlevel: {self.level}"
        frame += f"\nscore: {self.score}\n"

        # next & hold piece preview
        frame += self.draw_preview(self.next_piece, "Next")
        frame += self.draw_preview(self.hold_piece, "Hold")

        sys.stdout.write(frame)
        sys.stdout.flush()

    
    def draw_preview(self, piece, title):

        frame = f"{title}:\n"

        # for initial empty Hold preview (keeping fixed size frame to avoid terminal flickers)
        if piece is None:
            for _ in range(5):
                frame += "          \n"
            return frame
        
        # preview frame
        preview_h = 5
        preview_w = 5

        shape = piece.shape
        shape_h = len(shape)
        shape_w = len(shape[0])
        top_pad = (preview_h - shape_h) // 2
        left_pad = (preview_w - shape_w) // 2

        for r in range(preview_h):
            printing_line = ""
            for c in range(preview_w):
                sr = r - top_pad
                sc = c - left_pad
                if 0 <= sr < shape_h and 0 <= sc < shape_w and shape[sr][sc] == 1:
                    printing_line += COLORS[piece.color] + "██" + COLORS[0]
                else:
                    printing_line += "  "
            frame += printing_line + "\n"

        return frame + "\n"


    def get_input(self):

        while msvcrt.kbhit():
            
            key = msvcrt.getch().lower()

            if key == b' ':
                self.hard_drop()
            
            if key == b'c':
                self.hold()

            if key == b'z':
                self.try_rotate("ccw")

            elif key == b'x':
                self.try_rotate("cw")

            elif key == b'\xe0':  # arrow keys

                key = msvcrt.getch()

                if key == b'K':
                    if self.can_move('left'):
                        self.current_piece.col -= 1

                elif key == b'M':
                    if self.can_move('right'):
                        self.current_piece.col += 1

                elif key == b'P':
                    if self.can_move("down"):
                        self.current_piece.row += 1
        

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

            self.draw()
            time.sleep(0.08)


    def remove_rows(self, rows):
        for row in sorted(rows, reverse=True):
            del self.board[row]
        for _ in rows:
            self.board.insert(0, [0] * COLS)


    def spawn_piece(self):

        # selecting a random piece and creating it
        piece_data = random.choice(list(PIECES_DATA.values()))
        new_piece = Piece(piece_data, 0, 4)

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

        ghost_piece_data =  {"shape": [row[:] for row in self.current_piece.shape], "color": self.current_piece.color}
        ghost = Piece(ghost_piece_data, self.current_piece.row, self.current_piece.col)
 
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
        original_shape = self.current_piece.shape
        original_row = self.current_piece.row
        original_col = self.current_piece.col

        # temporary rotation
        self.current_piece.rotate(direction)

        # try wall kicking
        for dx, dy in WALL_KICKS:
            self.current_piece.row = original_row + dx
            self.current_piece.col = original_col + dy
            if self.can_move("neutral"):
                return True  # success

        # revert if all failed
        self.current_piece.shape = original_shape
        self.current_piece.row = original_row
        self.current_piece.col = original_col
        return False
                


def gameloop():

    tetris = Game()
    tetris.initialize_screen()
    last_fall_time = time.time()  

    while not tetris.game_over:

        # drawing current state
        tetris.draw()

        # keyboard input
        tetris.get_input()

        # skipping gravity, if fall interval is not completed yet
        # for updating rotation/movement before next
        current_time = time.time()
        if current_time - last_fall_time >= tetris.get_fall_interval():
            tetris.gravity()
            last_fall_time = current_time

        time.sleep(0.01)

    # show final spawning collision and GAMEOVER
    tetris.draw()
    print("GAME OVER!")


if __name__ == "__main__":
    gameloop()




"""
TO DO:
fater action when holding keyboard key
SRS for rotations

make README
game version releases in github

gui?
exe?
port app?

"""