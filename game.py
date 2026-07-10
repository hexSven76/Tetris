
from piece import Piece
from pieces_data import PIECES_DATA
from srs import JLSTZ_KICKS, I_KICKS
from constants import *
from renderer import Renderer
from input import InputHandler
from board import Board, Direction
import time
import random
from colorama import just_fix_windows_console
just_fix_windows_console()


class Game:
    
    def __init__(self):

        self.board = Board()
        self.input = InputHandler()
        self.bag = []
        self.current_piece = self.spawn_piece()
        self.next_piece = self.spawn_piece()
        self.score = 0
        self.total_lines = 0
        self.lock_timer = None
        self.lock_resets = 0
        self.level = START_LEVEL
        self.hold_piece = None
        self.can_hold = True
        self.paused = False 
        self.game_over = False


    def get_fall_interval(self):
        return max(0.03, 0.8 * (0.82 ** (self.level - 1)))
    

    def clear_lines(self):
        
        lines_cleared = self.board.get_completed_rows()
        if lines_cleared:
            self.animate_clearing_lines(lines_cleared)
            self.board.remove_rows(lines_cleared)
            lines = len(lines_cleared)
            self.score += lines * 100
            self.total_lines += lines
            self.level = START_LEVEL + self.total_lines // LINES_PER_LEVEL


    def animate_clearing_lines(self, rows):

        MIDDLE_LEFT = (COLS - 1) // 2
        MIDDLE_RIGHT = COLS // 2

        for offset in range(COLS // 2 + 1):
            for row in rows:

                left = MIDDLE_LEFT - offset
                right = MIDDLE_RIGHT + offset

                if 0 <= left < COLS:
                    self.board.grid[row][left] = 0
                if 0 <= right < COLS:
                    self.board.grid[row][right] = 0

            Renderer.draw(self)
            time.sleep(0.08)


    def spawn_piece(self):

        # poping a piece out of bag (if empty bag, refills it first)
        if not self.bag:
            self.refill_bag()
        piece_type = self.bag.pop()

        new_piece = Piece(piece_type, SPAWN_ROW, SPAWN_COL)

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
            if self.board.grid[row][col] != 0:
                return False

        return True
    

    def gravity(self):

        if self.board.can_move(self.current_piece, Direction.DOWN):
            self.current_piece.row += 1
            self.lock_timer = None
        else:
            if self.lock_timer is None:
                self.lock_timer = time.time()


    def hard_drop(self):

        while self.board.can_move(self.current_piece, Direction.DOWN):
            self.current_piece.row += 1
        self.lock_and_spawn()


    def lock_and_spawn(self):

        self.board.place_piece(self.current_piece)
        self.clear_lines()  # checking for lines to clear
        self.current_piece = self.next_piece
        self.lock_timer = None
        self.lock_resets = 0
        self.next_piece = self.spawn_piece()
        self.can_hold = True
        if not self.can_spawn(self.current_piece):
            self.game_over = True
            

    def get_ghost(self):

        ghost = Piece(self.current_piece.type, self.current_piece.row, self.current_piece.col)
        ghost.rotation = self.current_piece.rotation

        while self.board.can_move(ghost, Direction.DOWN):
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

            if self.board.can_move(self.current_piece, Direction.NEUTRAL):
                self.reset_lock_delay()
                return True

        # revert if failed
        piece.rotation = old_rotation
        piece.row = old_row
        piece.col = old_col
        return False
    

    def refill_bag(self):

        self.bag = list(PIECES_DATA.keys())
        random.shuffle(self.bag)
                
    
    def reset_lock_delay(self):

        if self.lock_timer is not None:
            if self.lock_resets < MAX_LOCK_RESETS:
                self.lock_timer = time.time()
                self.lock_resets += 1


    def toggle_pause(self):
        self.paused = not self.paused


"""
TO DO:

better terminal (high score, level, time)
themes
audio?

websocket
port?

"""