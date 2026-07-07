
from constants import ARR, DAS
from board import Direction
import time
from keys import Key
from keyboard import Keyboard

class InputHandler:

    def __init__(self):

        self.keyboard = Keyboard()
        self.prev_keys = {}
        self.horizontal_direction = 0   # -1 left | +1 right | 0 none
        self.last_horizontal_time = 0
        self.horizontal_started = 0
        self.down_pressed = False
        self.down_next_repeat = 0


    def update(self, game):
        
        current_time = time.time()

        # Horizontal movement 

        left = self.key_held(Key.LEFT)
        right = self.key_held(Key.RIGHT)

        direction = 0

        if left and not right:
            direction = -1
        elif right and not left:
            direction = 1

        if direction != self.horizontal_direction:

            self.horizontal_direction = direction
            self.das_start_time = current_time
            self.arr_last_move_time = current_time

            # Immediate move
            if direction == -1 and game.board.can_move(game.current_piece, Direction.LEFT):
                game.current_piece.col -= 1

            elif direction == 1 and game.board.can_move(game.current_piece, Direction.RIGHT):
                game.current_piece.col += 1

        elif direction != 0:

            if current_time - self.das_start_time >= DAS:

                if current_time - self.arr_last_move_time >= ARR:

                    if direction == -1 and game.board.can_move(game.current_piece, Direction.LEFT):
                        game.current_piece.col -= 1

                    elif direction == 1 and game.board.can_move(game.current_piece, Direction.RIGHT):
                        game.current_piece.col += 1

                    self.arr_last_move_time = current_time

        else:
            self.horizontal_direction = 0

        # Soft Drop 

        if self.key_held(Key.DOWN):

            if not self.down_pressed:
                if game.board.can_move(game.current_piece, Direction.DOWN):
                    game.current_piece.row += 1
                self.down_pressed = True
                self.down_next_repeat = time.time() + DAS

            elif time.time() >= self.down_next_repeat:
                if game.board.can_move(game.current_piece, Direction.DOWN):
                    game.current_piece.row += 1
                self.down_next_repeat += ARR

        else:
            self.down_pressed = False

        # single-take keys 

        if self.key_pressed(Key.Z):
            game.try_rotate("ccw")

        if self.key_pressed(Key.X):
            game.try_rotate("cw")

        if self.key_pressed(Key.C):
            game.hold()

        if self.key_pressed(Key.SPACE):
            game.hard_drop()
    

    def key_held(self, key):
        return self.keyboard.key_held(key)
    

    def key_pressed(self, key):
        down = self.key_held(key)
        was_down = self.prev_keys.get(key, False)
        self.prev_keys[key] = down
        return down and not was_down
