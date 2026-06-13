import time
import msvcrt
from piece import Piece, PIECES_DATA

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
            temp_board[row][col] = 1

        # printing temp_board with occupied cells filled  (□ or · for empty cells?!)
        for row in temp_board:
            for cell in row:
                print("■" if cell!=0 else "□", end="")
            print()

        print(f"\n score: {self.score}")
    

    def get_input(self):

        while msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b'\xe0':

                key = msvcrt.getch()

                if key == b'K':
                    if self.can_move('left'):
                        self.current_piece.col -= 1
                        self.draw()

                elif key == b'M':
                    if self.can_move('right'):
                        self.current_piece.col += 1
                        self.draw()

                elif key == b'H': 
                    old_shape = self.current_piece.shape
                    self.current_piece.rotate()
                    if not self.can_move('rotated'):
                        self.current_piece.shape = old_shape
                    self.draw()

                elif key == b'P':
                    # soft drop
                    pass

                elif key == b'????????':  # spacebar
                    # hard drop
                    pass
        

    def can_move(self, direction):
    
        def get_offsets(direction):
            if direction == "down":
                return 1, 0
            if direction == "right":
                return 0, 1
            if direction == "left":
                return 0, -1
            if direction == "rotated":
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
            self.board[row][col] = 1
        
        # checking for lines to clear
        self.clear_lines()


    def clear_lines(self):

        lines_cleared = 0
        row = ROWS - 1
        
        while row >= 0:
            if all(cell == 1 for cell in self.board[row]):
                del self.board[row]
                self.board.insert(0, [0 for _ in range(COLS)])
                lines_cleared += 1
            else:
                row -= 1

        self.score += lines_cleared * 100


    def spawn_piece(self):  #unfinished
        # random initial rotation (later)
        import random
        piece_data = random.choice(list(PIECES_DATA.values()))
        new_piece = Piece(piece_data, 0, 4) 
        return new_piece
    

    def can_spawn(self): # unfinished
        # checking whether any occupied cell of spawning-piece is empty in board
        return True #temp
    

    def gravity(self):

        if self.can_move("down"):
            self.current_piece.row += 1
        else:
            # permenantly placing the piece on bottom
            self.place_piece()
            new_piece = self.spawn_piece()

            if self.can_spawn():
                self.current_piece = new_piece
            else:
                # game over if new piece immediately collides with older pieces
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

    print(f"GAME OVER ! SCORE: {tetris.score} \n")


if __name__ == "__main__":
    gameloop()




"""
TO DO:
spawn_piece()
can_spawn()
get_input() Soft drop
get_input() Hard drop
slow animation for clearing lines ?!
Z and X for clock/counter-clock rotation
colored pieces
S and Z piece are still freaky in rotation

"""