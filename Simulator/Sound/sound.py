import pygame
import threading


class Sound:
    @staticmethod
    def load():
        pygame.mixer.init()
        filename_song = 'Sound/SoundResource/world.execute(me);.mp3'
        pygame.mixer.music.load(filename_song)

    @staticmethod
    def play():
        pygame.mixer.music.play()

    @staticmethod
    def pause():
        pygame.mixer.music.pause()

    @staticmethod
    def stop():
        pygame.mixer.music.stop()
