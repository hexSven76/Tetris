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
from piece import Piece, PIECES_DATA, COLORS

COLS = 10
ROWS = 20
FALL_INTERVAL = 0.28

class Game:
    
    def __init__(self):
        self.board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.current_piece = self.spawn_piece()
        self.next_piece = self.spawn_piece()    
        self.score = 0
        self.game_over = False


    def initialize_screen(self):
        print("\033[2J", end="")   # clear terminal
        print("\033[?25l", end="") # hide cursor


    def draw(self):

        print("\033[H", end="")
        temp_board = [row[:] for row in self.board]

        # getting ghost piece and marking it on temp_board
        ghost = self.get_ghost()
        for row, col in ghost.get_occupied_cells():
            if 0 <= row < ROWS and 0 <= col < COLS:
                temp_board[row][col] = -1

        # getting occupied cells and marking them on temp_board
        for row, col in self.current_piece.get_occupied_cells():
            temp_board[row][col] = self.current_piece.color

        # printing temp_board with occupied cells filled
        RESET = "\033[0m"
        GHOST = "\033[90m"
        for row in temp_board:
            printing_line = ""
            for cell in row:
                if cell == 0:
                    printing_line += "  "
                elif cell == -1:
                    printing_line += GHOST + "░░" + RESET
                else:
                    printing_line += COLORS[cell] + "██" + RESET

            # side borders
            print("│" + printing_line + "│")

        # lower border  
        print("└" + "─" * (COLS * 2) + "┘")

        # next piece
        preview_h = 5
        preview_w = 5
        shape = self.next_piece.shape
        shape_h = len(shape)
        shape_w = len(shape[0])
        top_pad = (preview_h - shape_h) // 2
        left_pad = (preview_w - shape_w) // 2

        print("Next: ")
        for r in range(preview_h):
            printing_line = ""
            for c in range(preview_w):
                sr = r - top_pad
                sc = c - left_pad
                if 0 <= sr < shape_h and 0 <= sc < shape_w and shape[sr][sc] == 1:
                    printing_line += COLORS[self.next_piece.color] + "██" + RESET
                else:
                    printing_line += "  "
            print(printing_line)

        print(f"\nscore: {self.score}")
    

    def get_input(self):

        while msvcrt.kbhit():
            
            key = msvcrt.getch().lower()

            if key == b' ':
                self.hard_drop()

            if key == b'z':
                old_shape = self.current_piece.shape
                self.current_piece.rotate("ccw")
                if not self.can_move("neutral"):
                    self.current_piece.shape = old_shape

            elif key == b'x':
                old_shape = self.current_piece.shape
                self.current_piece.rotate("cw")
                if not self.can_move("neutral"):
                    self.current_piece.shape = old_shape

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

        lines_cleared = 0
        row = ROWS - 1
        
        while row >= 0:
            if all(cell != 0 for cell in self.board[row]):
                del self.board[row]
                self.board.insert(0, [0 for _ in range(COLS)])
                lines_cleared += 1
            else:
                row -= 1

        self.score += lines_cleared * 100


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
        if not self.can_spawn(self.current_piece):
            self.game_over = True
            

    def get_ghost(self):

        ghost_piece_data =  {"shape": [row[:] for row in self.current_piece.shape], "color": self.current_piece.color}
        ghost = Piece(ghost_piece_data, self.current_piece.row, self.current_piece.col)
 
        while self.can_move_piece(ghost, "down"):
            ghost.row += 1

        return ghost
                


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
        if current_time - last_fall_time >= FALL_INTERVAL:
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
fix terminal
slow animation for clearing lines ?!
gui?
exe?
port app?

"""