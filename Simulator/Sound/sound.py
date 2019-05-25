import pygame
import wave
import threading
import numpy as np
import pylab
import struct
import io
from PIL import Image
import sounddevice as sd


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
        # crop = image
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
        # y = abs(np.fft.fft(y) * self.nchannels)
        y = y[:len(y)//2]
        # pylab.specgram(y, NFFT=1024, Fs=self.framerate, noverlap=900)
        pylab.plt.ylim(-32768, 32768)
        pylab.plot(range(count//2), y)
        pylab.savefig(data)
        data.seek(0)
        image = Image.open(data)
        crop = image.crop((81, 59, 575, 426))
        # crop = image
        return crop

    @staticmethod
    def blend(sp1, sp2, count: int):
        im1 = sp1.map(count, clear=True)
        im2 = sp2.raw(count, clear=False)
        res = Image.blend(im1, im2, 0.5)
        return res


# 处理音频频谱 - 尝试实时录音
#   0 Microsoft 声音映射器 - Output, MME (0 in, 2 out)
# < 1 扬声器 (Realtek High Definition, MME (0 in, 2 out)
#   2 主声音驱动程序, Windows DirectSound (0 in, 2 out)
#   3 扬声器 (Realtek High Definition Audio), Windows DirectSound (0 in, 2 out)
#   4 扬声器 (Realtek High Definition Audio), Windows WASAPI (0 in, 2 out)
#   5 Speakers (Realtek HD Audio output), Windows WDM-KS (0 in, 6 out)
#   6 立体声混音 (Realtek HD Audio Stereo input), Windows WDM-KS (2 in, 0 out)
#   7 线路输入 (Realtek HD Audio Line input), Windows WDM-KS (2 in, 0 out)
#   8 FrontMic (Realtek HD Audio Front Mic input), Windows WDM-KS (2 in, 0 out)
#   9 麦克风 (Realtek HD Audio Mic input), Windows WDM-KS (2 in, 0 out)

# fs = 44100 # Hz
# length = 5 # s
# recording = sd.rec(frames=fs * length, samplerate=fs, blocking=True, channels=1)
class SpectrumMap2:
    def __init__(self):
        devices = sd.query_devices()
        device = 11
        for i in range(len(devices)):
            d = devices[i]
            if '立体声混音' in d['name']:
                device = i
        sd.default.device[0] = device
        print('采用', devices[device]['name'], '录音')

        self.nchannels = 1
        self.framerate = 44100

    def record(self, period: float):
        recording = sd.rec(frames=int(self.framerate * period),
                           samplerate=self.framerate, blocking=True, channels=self.nchannels, dtype='int16')
        return recording.reshape((recording.size, ))

    def map(self, ndata, clear: bool=True):
        if clear:
            pylab.plt.clf()
        y = ndata

        data = io.BytesIO()
        pylab.specgram(y, NFFT=32, Fs=self.framerate, noverlap=18)
        pylab.savefig(data)
        data.seek(0)
        image = Image.open(data)
        # crop = image.crop((81, 59, 575, 426))
        crop = image
        return crop

    @staticmethod
    def raw(ndata, clear: bool=True):
        if clear:
            pylab.plt.clf()
        y = ndata
        count = len(ndata)

        data = io.BytesIO()
        # y = abs(np.fft.fft(y) * self.nchannels)
        y = y[:len(y)//2]
        pylab.plt.ylim(-32768, 32768)
        pylab.plot(range(count//2), y)
        pylab.savefig(data)
        data.seek(0)
        image = Image.open(data)
        # crop = image.crop((81, 59, 575, 426))
        crop = image
        return crop

    # @staticmethod
    # def blend(sp1, sp2, ndata):
    #     im1 = sp1.map(ndata, clear=True)
    #     im2 = sp2.raw(ndata, clear=False)
    #     res = Image.blend(im1, im2, 0.5)
    #     return res

    def fetch(self, period: float):
        ndata = self.record(period)
        # im1 = self.map(ndata, clear=True)
        im2 = self.raw(ndata, clear=True)
        # res = Image.blend(im1, im2, 0.5)
        res = im2
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
