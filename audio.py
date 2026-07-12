
from constants import SFX_VOLUME
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

class Audio:

    enabled = True
    sounds = {}

    @staticmethod
    def initialize():

        if not Audio.enabled:
            return
        pygame.mixer.init()


    @staticmethod
    def shutdown():

        if Audio.enabled:
            pygame.mixer.quit()


    @staticmethod
    def load():
        
        if not Audio.enabled:
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

        if not Audio.enabled:
            return
        if name in Audio.sounds:
            Audio.sounds[name].play()
