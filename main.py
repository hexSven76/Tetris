
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

    tetris = Game()
    Renderer.initialize_screen()
    last_fall_time = time.time()  

    while not tetris.game_over:

        # drawing current state
        Renderer.draw(tetris)

        # keyboard input
        tetris.input.update(tetris)

        # skipping gravity, if fall interval is not completed yet
        # for updating rotation/movement before next
        current_time = time.time()
        if current_time - last_fall_time >= tetris.get_fall_interval():
            tetris.gravity()
            last_fall_time = current_time

        time.sleep(0.01)

    # show final spawning collision and GAMEOVER
    Renderer.draw(tetris)
    print("GAME OVER!")


if __name__ == "__main__":
    gameloop()