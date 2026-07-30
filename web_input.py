from constants import ARR, DAS
from board import Direction
import time


class WebInputHandler:

    def __init__(self):

        self.held = {"left": False, "right": False, "down": False}
        self.pending_actions = []  # single-shot actions queued by the client
        self.horizontal_direction = 0   # -1 left | +1 right | 0 none
        self.das_start_time = 0
        self.arr_last_move_time = 0
        self.down_pressed = False
        self.down_next_repeat = 0


    # --- called from Flask request handlers, whenever a browser key event arrives ---

    def apply_event(self, action):

        if action == "left_down":
            self.held["left"] = True
        elif action == "left_up":
            self.held["left"] = False
        elif action == "right_down":
            self.held["right"] = True
        elif action == "right_up":
            self.held["right"] = False
        elif action == "down_down":
            self.held["down"] = True
        elif action == "down_up":
            self.held["down"] = False
        elif action in ("rotate_cw", "rotate_ccw", "hold", "hard_drop", "pause"):
            self.pending_actions.append(action)


    # --- called once per tick from the background game loop ---

    def update(self, game):

        # pause can be toggled even while paused
        if "pause" in self.pending_actions:
            game.toggle_pause()
        self.pending_actions = [a for a in self.pending_actions if a != "pause"]

        if game.paused:
            self.pending_actions.clear()
            return

        current_time = time.time()

        # Horizontal movement

        left = self.held["left"]
        right = self.held["right"]

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

        # Soft drop

        if self.held["down"]:

            if not self.down_pressed:
                if game.board.can_move(game.current_piece, Direction.DOWN):
                    game.current_piece.row += 1
                self.down_pressed = True
                self.down_next_repeat = current_time + DAS

            elif current_time >= self.down_next_repeat:
                if game.board.can_move(game.current_piece, Direction.DOWN):
                    game.current_piece.row += 1
                self.down_next_repeat += ARR

        else:
            self.down_pressed = False

        # Single-shot actions (already edge-triggered client-side via event.repeat filtering)

        actions = self.pending_actions
        self.pending_actions = []

        for action in actions:
            if action == "rotate_ccw":
                game.try_rotate("ccw")
            elif action == "rotate_cw":
                game.try_rotate("cw")
            elif action == "hold":
                game.hold()
            elif action == "hard_drop":
                game.hard_drop()
