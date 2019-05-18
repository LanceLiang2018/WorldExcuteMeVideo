import pygame
import wave
import threading
import numpy as np
import pylab
import struct
import io
from PIL import Image


# 处理音频频谱
# voice.wav 格式：8000 rate 16bit 单声道
class SpectrumMap:
    def __init__(self):
        FILENAME = 'Sound/SoundResource/voice.wav'
        self.wavefile = wave.open(FILENAME, 'r')

        self.nchannels = self.wavefile.getnchannels()
        self.sample_width = self.wavefile.getsampwidth()
        self.framerate = self.wavefile.getframerate()
        self.numframes = self.wavefile.getnframes()

    def seek(self, frame: int):
        self.wavefile.setpos(frame)

    def map(self, count: int):
        y = np.zeros(count)

        for i in range(count):
            val = self.wavefile.readframes(1)
            left = val[0:2]
            v = struct.unpack('h', left)[0]
            y[i] = v

        data = io.BytesIO()
        pylab.specgram(y, NFFT=1024, Fs=self.framerate, noverlap=900)
        pylab.savefig(data)
        data.seek(0)
        image = Image.open(data)
        return image

    def raw(self, count):
        y = np.zeros(count)

        for i in range(count):
            val = self.wavefile.readframes(1)
            left = val[0:2]
            v = struct.unpack('h', left)[0]
            y[i] = v

        data = io.BytesIO()
        # pylab.specgram(y, NFFT=1024, Fs=self.framerate, noverlap=900)
        pylab.plot(range(count), y)
        pylab.savefig(data)
        data.seek(0)
        image = Image.open(data)
        return image

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
