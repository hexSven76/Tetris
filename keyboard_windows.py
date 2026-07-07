
from ctypes import windll
from input import Key
from keys import Key

KEY_MAP = {
    Key.LEFT: 0x25,
    Key.RIGHT: 0x27,
    Key.DOWN: 0x28,
    Key.SPACE: 0x20,
    Key.Z: ord("Z"),
    Key.X: ord("X"),
    Key.C: ord("C"),
}

class Keyboard:

    def key_held(self, key):
        vk = KEY_MAP[key]
        return bool(windll.user32.GetAsyncKeyState(vk) & 0x8000)
