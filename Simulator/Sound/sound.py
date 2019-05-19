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

    def map(self, count: int, clear: bool=True):
        if clear:
            pylab.plt.clf()
        y = np.zeros(count)

        for i in range(count):
            val = self.wavefile.readframes(1)
            left = val[0:2]
            try:
                v = struct.unpack('h', left)[0]
                y[i] = v
            except struct.error:
                pass

        data = io.BytesIO()
        pylab.specgram(y, NFFT=32, Fs=self.framerate, noverlap=18)
        pylab.savefig(data)
        data.seek(0)
        image = Image.open(data)
        crop = image.crop((81, 59, 575, 426))
        return crop

    def raw(self, count, clear: bool=True):
        if clear:
            pylab.plt.clf()
        y = np.zeros(count)

        for i in range(count):
            val = self.wavefile.readframes(1)
            left = val[0:2]
            try:
                v = struct.unpack('h', left)[0]
                y[i] = v
            except struct.error:
                pass

        data = io.BytesIO()
        y = abs(np.fft.fft(y) * self.nchannels)
        y = y[:len(y)//2]
        # pylab.specgram(y, NFFT=1024, Fs=self.framerate, noverlap=900)
        pylab.plot(range(count//2), y)
        pylab.savefig(data)
        data.seek(0)
        image = Image.open(data)
        crop = image.crop((81, 59, 575, 426))
        return crop

    @staticmethod
    def blend(sp1, sp2, count: int):
        im1 = sp1.map(count, clear=True)
        im2 = sp2.raw(count, clear=False)
        res = Image.blend(im1, im2, 0.5)
        return res


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
