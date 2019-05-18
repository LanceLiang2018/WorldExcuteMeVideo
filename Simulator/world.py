from tkinter import *
from Simulator.Lyric.lyric import *
from Simulator.Me import *
from Simulator.Render import *
from Simulator.Sound.sound import *
from Simulator.ui_logger import UiLogger
import random
from PIL import Image, ImageTk


class World:
    def __init__(self, root=None):
        self.root = root
        if self.root is None:
            self.root = Tk()

        self.title = 'World Simulator'
        self.new_title(self.title)

        # 一些基本类
        self.spectrum_map = SpectrumMap()

        # 在这里构建窗口

        frame_left = Frame(self.root)
        frame_right = Frame(self.root)

        # 音频频谱表现
        im = self.spectrum_map.map(1024*10)
        imp = ImageTk.PhotoImage(image=im)
        self.voice = Label(frame_right, image=imp)
        self.voice.image = imp
        self.voice.grid(row=1, column=0, sticky=W+E)

        # Me说的话
        self.words = UiLogger(frame_right, title='I said', max_height=15)
        self.words.logger().grid(row=2, column=0, sticky=W + E)

        # My Status
        self.words = UiLogger(frame_right, title='Status', max_height=15)
        self.words.logger().grid(row=2, column=0, sticky=W + E)

        # 程序运行日志
        self.log = UiLogger(frame_right, title='Logs', max_height=10)
        self.log.logger().grid(row=3, column=0, sticky=W+E)

        frame_left.pack(side=LEFT)
        frame_right.pack(side=RIGHT)

        self.thread()

    def new_title(self, title: str):
        self.title = title
        self.root.title(self.title)

    # def thread(self):
    #     # self.logger.push(UiLogger.Item(random.randint(0, 4), 'create', 'World No.%s' % random.randint(0, 9999)))
    #     if self.lrc.has_new():
    #         self.logger.push(UiLogger.Item(UiLogger.LEVEL_INFO, 'Lyric', self.lrc.next()))
    #     self.root.after(10, self.thread)

    def thread(self):
        im = self.spectrum_map.raw(1024 * 10)
        imp = ImageTk.PhotoImage(image=im)
        self.voice.configure(image=imp)
        self.voice.image = imp

        self.root.after(100, self.thread)

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    _world = World()
    _world.mainloop()
