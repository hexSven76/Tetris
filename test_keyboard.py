
from keyboard import Keyboard
from keys import Key
import time

keyboard = Keyboard()

while True:

    if keyboard.key_held(Key.LEFT):
        print("LEFT")

    if keyboard.key_held(Key.Z):
        print("Z")

    time.sleep(0.05)