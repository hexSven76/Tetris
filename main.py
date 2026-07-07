
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
import time

def gameloop():

    try:
        tetris = Game()
        Renderer.initialize_screen()
        last_fall_time = time.time()  

        while not tetris.game_over:

            # rendering current state
            Renderer.draw(tetris)

            # keyboard input
            tetris.input.update(tetris)

            # skipping gravity, if fall interval is not completed yet
            # (for updating rotation/movement before next gravity proc)
            current_time = time.time()
            if current_time - last_fall_time >= tetris.get_fall_interval():
                tetris.gravity()
                last_fall_time = current_time

            time.sleep(0.01)

        # show final spawning collision and GAMEOVER
        Renderer.draw(tetris)
        print("GAME OVER!")
        Renderer.restore_screen()

    finally:
        Renderer.restore_screen()


if __name__ == "__main__":
    gameloop()