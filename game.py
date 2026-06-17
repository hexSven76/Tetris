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
        self.score = 0
        self.game_over = False


    def initialize_screen(self):
        print("\033[2J", end="")   # clear terminal
        print("\033[?25l", end="") # hide cursor


    def draw(self):

        print("\033[H", end="") # cleart terminal
        temp_board = [row[:] for row in self.board]

        # getting occupied cells and marking them on temp_board
        for row, col in self.current_piece.get_occupied_cells():
            temp_board[row][col] = self.current_piece.color

        # printing temp_board with occupied cells filled
        RESET = "\033[0m"
        for row in temp_board:

            printing_line = ""

            for cell in row:
                if cell == 0:
                    printing_line += "  "
                else:
                    printing_line += COLORS[cell] + "██" + RESET

            # side borders
            print("│" + printing_line + "│")

       # lower border  
        print("└" + "─" * (COLS * 2) + "┘")

        print()
        print(f"\n score: {self.score}")
    

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
                self.draw()

            elif key == b'x':
                old_shape = self.current_piece.shape
                self.current_piece.rotate("cw")
                if not self.can_move("neutral"):
                    self.current_piece.shape = old_shape
                self.draw()

            elif key == b'\xe0':  # arrow keys

                key = msvcrt.getch()

                if key == b'K':
                    if self.can_move('left'):
                        self.current_piece.col -= 1
                        self.draw()

                elif key == b'M':
                    if self.can_move('right'):
                        self.current_piece.col += 1
                        self.draw()

                elif key == b'P':
                    if self.can_move("down"):
                        self.current_piece.row += 1
        

    def can_move(self, direction):
    
        def get_offsets(direction):
            if direction == "down":
                return 1, 0
            if direction == "right":
                return 0, 1
            if direction == "left":
                return 0, -1
            if direction == "neutral":
                return 0, 0
            
        for row, col in self.current_piece.get_occupied_cells():

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
        for i in range(random_initial_rotation):
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
        self.current_piece = self.spawn_piece()
        if not self.can_spawn(self.current_piece):
            self.game_over = True
                


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
see next spawning piece
shadow
slow animation for clearing lines ?!
S and Z pieces are still freaky in rotation
gui?
exe?
port app?

"""