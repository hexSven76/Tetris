
from constants import *

class Board:
    
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]


    def can_move(self, piece, direction):
    
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

            dx, dy = get_offsets(direction)
            target_row = row + dx
            target_col = col + dy

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
            if self.grid[target_row][target_col] != 0:
                return False
    
        return True
    

    def place_piece(self, piece):
        # getting occupied cells & permenantly marking it on main board
        for row, col in piece.get_occupied_cells():
            self.grid[row][col] = piece.color
        
        # checking for lines to clear
        # self.clear_lines()


    def get_completed_rows(self):

        full_rows = []

        for r in range(ROWS):
            if all(cell != 0 for cell in self.grid[r]):
                full_rows.append(r)

        return full_rows


    def remove_rows(self, rows):

        for r in sorted(rows, reverse=True):
            del self.grid[r]
            
        for _ in rows:
            self.grid.insert(0, [0] * COLS)
