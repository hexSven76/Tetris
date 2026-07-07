
from constants import ROWS, COLS, COLORS
import sys

class Renderer:

    @staticmethod
    def initialize_screen():
        sys.stdout.write("\033[?1049h")  # switch to alternate buffer
        sys.stdout.write("\033[?25l")    # hide cursor
        sys.stdout.flush()


    @staticmethod
    def restore_screen(self):
        sys.stdout.write("\033[?1049l")  # return from alternate buffer
        sys.stdout.write("\033[?25h")    # show cursor
        sys.stdout.flush()


    @staticmethod
    def draw(game):

        # concating everything in one string to print it once
        frame = "\033[H\033[0J"
        temp_board = [row[:] for row in game.board.grid]

        # getting ghost piece and marking it on temp_board
        ghost = game.get_ghost()
        for row, col in ghost.get_occupied_cells():
            if 0 <= row < ROWS and 0 <= col < COLS:
                temp_board[row][col] = -1

        # getting occupied cells and marking them on temp_board
        for row, col in game.current_piece.get_occupied_cells():
            temp_board[row][col] = game.current_piece.color

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
        frame += f"\nlevel: {game.level}"
        frame += f"\nscore: {game.score}\n"

        # next & hold piece preview
        frame += Renderer.piece_preview(game.next_piece, "Next")
        frame += Renderer.piece_preview(game.hold_piece, "Hold")

        sys.stdout.write(frame)
        sys.stdout.flush()


    @staticmethod
    def piece_preview(piece, title):

        frame = f"{title}:\n"

        # for initial empty Hold preview (keeping fixed size frame to avoid terminal flickers)
        if piece is None:
            for _ in range(5):
                frame += "          \n"
            return frame

        # preview frame
        preview_h = 5
        preview_w = 5

        shape = piece.get_shape()
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
