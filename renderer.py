
from constants import ROWS, COLS
from themes import colors
import sys

class Renderer:

    @staticmethod
    def initialize_screen():
        sys.stdout.write("\033[?1049h")  # switch to alternate buffer
        sys.stdout.write("\033[?25l") # hide cursor
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

        # getting board ad side seperately and printing together (to show stats next to board)
        board_lines = Renderer.draw_board(temp_board)
        side_lines = Renderer.draw_sidebar(game)

        for i in range(max(len(board_lines), len(side_lines))):
            left = board_lines[i] if i < len(board_lines) else ""
            right = side_lines[i] if i < len(side_lines) else ""

            frame += left + "     " + right + "\n"

        sys.stdout.write(frame)
        sys.stdout.flush()


    @staticmethod
    def draw_board(temp_board):

        printing_line = []

        # top border
        printing_line.append("┌" + "─" * (COLS * 2) + "┐")

        # printing temp_board with occupied cells filled
        for row in temp_board:
            lines = ""
            for cell in row:
                if cell == 0:
                    lines += "  "
                elif cell == -1:
                    lines += colors()[-1] + "░░" + colors()[0]
                else:
                    lines += colors()[cell] + "██" + colors()[0]

            # side borders
            printing_line.append("│" + lines + "│")
        
        # lower border  
        printing_line.append("└" + "─" * (COLS * 2) + "┘")
        return printing_line
    

    @staticmethod
    def draw_sidebar(game):

        printing_line = []
        printing_line.append(f"Lines:        {game.total_lines}")
        printing_line.append(f"Level:        {game.level}")
        printing_line.append(f"Score:        {game.score}")
        printing_line.append(f"High Score:   {game.high_score}")

        seconds = game.get_elapsed_time()
        minutes = seconds // 60
        seconds = seconds % 60
        printing_line.append(f"Time:         {minutes:02}:{seconds:02}")

        printing_line.append("")

        printing_line.append("Next:")
        next_preview = Renderer.piece_preview(game.next_piece, "")
        printing_line.extend(next_preview.rstrip("\n").split("\n"))

        printing_line.append("")

        printing_line.append("Hold:")
        hold_preview = Renderer.piece_preview(game.hold_piece, "")
        printing_line.extend(hold_preview.rstrip("\n").split("\n"))

        if game.paused:
            printing_line.append("")
            printing_line.append("  PAUSED")
            printing_line.append(" Press P")

        return printing_line


    @staticmethod
    def piece_preview(piece, title):

        frame = ""

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
                    printing_line += colors()[piece.color] + "██" + colors()[0]
                else:
                    printing_line += "  "
            frame += printing_line + "\n"

        return frame + "\n"
