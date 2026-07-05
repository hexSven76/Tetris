
COLS = 10
ROWS = 20

START_LEVEL = 8
LINES_PER_LEVEL = 10

DAS = 0.15   # seconds before auto-repeat starts
ARR = 0.04   # seconds between repeated moves

SPAWN_COL = 4
SPAWN_ROW = 0
PREVIEW_BOX_SIZE = 5

# ANSI terminal colors
COLORS = {
   -1: "\033[90m",  # light-gray (for ghost piece)
    0: "\033[0m",   # no color (for reseting)
    1: "\033[36m",  # cyan
    2: "\033[33m",  # yellow
    3: "\033[35m",  # pink
    4: "\033[32m",  # green
    5: "\033[31m",  # red
    6: "\033[34m",  # blue
    7: "\033[93m"   # orange
}
