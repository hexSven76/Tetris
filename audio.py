
from constants import SFX_VOLUME
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"

try:
    import pygame
except ImportError:
    # pygame isn't required for frontends that don't need server-side sound
    pygame = None

class Audio:

    enabled = True
    sounds = {}

    @staticmethod
    def initialize():

        if not Audio.enabled or pygame is None:
            return
        pygame.mixer.init()


    @staticmethod
    def shutdown():

        if Audio.enabled and pygame is not None:
            pygame.mixer.quit()


    @staticmethod
    def load():
        
        if not Audio.enabled or pygame is None:
            return
        
        sound_folder = os.path.join("assets", "sounds")

        for name in os.listdir(sound_folder):
            if name.endswith(".wav"):
                key = name.replace(".wav", "")
                sound = pygame.mixer.Sound(os.path.join(sound_folder, name))
                sound.set_volume(SFX_VOLUME)
                Audio.sounds[key] = sound


    @staticmethod
    def play(name):

        if not Audio.enabled or pygame is None:
            return
        if name in Audio.sounds:
            Audio.sounds[name].play()
