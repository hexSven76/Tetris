
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


from game import Game
from renderer import Renderer
from constants import LOCK_DELAY
from audio import Audio
import time

Audio.initialize()
Audio.load()

def gameloop():

    tetris = Game()
    Renderer.initialize_screen()
    last_fall_time = time.time()  

    while not tetris.game_over:

        # rendering current state
        if not tetris.paused:
            Renderer.draw(tetris)

        # keyboard input
        tetris.input.update(tetris)

        # continue if game isn't paused
        if not tetris.paused:
            
            # skipping gravity, if fall interval is not completed yet
            # (for updating rotation/movement before next gravity proc)
            current_time = time.time()
            if current_time - last_fall_time >= tetris.get_fall_interval():
                tetris.gravity()
                last_fall_time = current_time

            if tetris.lock_timer:
                if current_time - tetris.lock_timer >= LOCK_DELAY:
                    tetris.lock_and_spawn()
         
        else:
            last_fall_time = time.time()

        time.sleep(0.01)

    # finishing the game
    tetris.end_game()


if __name__ == "__main__":
    gameloop()
    