
import sys
import termios
import tty
import select
from keys import Key

KEY_MAP = {
    "z": Key.Z,
    "x": Key.X,
    "c": Key.C,
    " ": Key.SPACE,
}

class Keyboard:

    def __init__(self):

        self.current_keys = set()
        self.old_settings = termios.tcgetattr(sys.stdin)
        tty.setcbreak(sys.stdin.fileno())


    def key_held(self, key):
        self.read_keys()
        return key in self.current_keys


    def read_keys(self):

        self.current_keys.clear()

        while select.select([sys.stdin], [], [], 0)[0]:

            char = sys.stdin.read(1)

            # arrows
            if char == "\x1b":

                seq = sys.stdin.read(2)

                if seq == "[D":
                    self.current_keys.add(Key.LEFT)

                elif seq == "[C":
                    self.current_keys.add(Key.RIGHT)

                elif seq == "[B":
                    self.current_keys.add(Key.DOWN)

            elif char in KEY_MAP:
                self.current_keys.add(KEY_MAP[char])


    def close(self):

        termios.tcsetattr(
            sys.stdin,
            termios.TCSADRAIN,
            self.old_settings
        )