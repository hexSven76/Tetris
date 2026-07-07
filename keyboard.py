
import platform

if platform.system() == "Windows":
    from keyboard_windows import Keyboard
else:
    from keyboard_linux import Keyboard