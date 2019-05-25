from tkinter import *
from Simulator.Lyric.lyric import *
from Simulator.Me import *
# from Simulator.Render import *
from Simulator.Sound.sound import *
from Simulator.ui_logger import UiLogger
# from Simulator.PPT3D.PPT import *
from Simulator.PPT3D.ppt3d import Page, Frame as mFrame, PPT, PPT3D
import random
from PIL import Image, ImageTk
import multiprocessing


class World:
    def __init__(self, root=None):
        self.root = root
        if self.root is None:
            self.root = Tk()

        self.title = 'World Simulator'
        self.new_title(self.title)

        # 一些基本类
        self.spectrum_map = SpectrumMap()
        self.spectrum_map_wave = SpectrumMap()
        self.lrc = Lyric()
        self.sound = Sound()

        # 在这里构建窗口

        frame_left = Frame(self.root)
        frame_right = Frame(self.root)

        # 音频频谱表现
        # im = self.spectrum_map.map(1024*10)
        # imp = ImageTk.PhotoImage(image=im)
        # self.voice = Label(frame_right, image=imp)
        self.voice = Label(frame_right)
        # self.voice.image = imp
        self.voice.grid(row=1, column=0, sticky=W+E)

        # Me说的话
        self.words = UiLogger(frame_right, title='I said', max_height=8)
        self.words.logger().grid(row=2, column=0, sticky=W + E)

        # My Status
        self.words = UiLogger(frame_right, title='Status', max_height=10)
        self.words.logger().grid(row=3, column=0, sticky=W + E)

        # 程序运行日志
        self.log = UiLogger(frame_right, title='Logs', max_height=5)
        self.log.logger().grid(row=4, column=0, sticky=W+E)

        # 占位窗口
        # self.span = UiLogger(frame_left, title='Simulation', max_height=22, width=600, height=300)
        # self.span.logger().grid(row=1, column=1, sticky=W+E, columnspan=2)
        self.span = LabelFrame(frame_left, text='Simulation', width=800, height=600)
        self.span.grid(row=1, column=1, sticky=W + E, columnspan=2)

        # 处理中
        self.processing = UiLogger(frame_left, title='Processing', max_height=5)
        self.processing.logger().grid(row=2, column=1, sticky=W+E)

        # 数据
        self.data = UiLogger(frame_left, title='Data', max_height=5)
        self.data.logger().grid(row=2, column=2, sticky=W+E)

        # frame_left.configure(width=600)
        # frame_left['width'] = 600

        frame_left.pack(side=LEFT)
        frame_right.pack(side=RIGHT)

        # im = self.spectrum_map.map(1024, clear=True)
        # im.save('spectrum_map.png')

        # 处理3D窗口
        self.ppt = PPT()
        page = Page()
        page.frames.append(mFrame(image=Image.new("RGBA", (128, 128))))
        page.position.load([random.random() * 6.8 for i in range(3)])
        self.ppt.pages.append(page)
        self.ppt3d = None
        t = threading.Thread(target=self.gl_mainloop)
        t.setDaemon(True)
        t.start()
        # p = multiprocessing.Process(target=self.gl_mainloop)
        # p.daemon = True
        # p.start()

        # self.thread()
        t = threading.Thread(target=self.thread)
        t.setDaemon(True)
        t.start()

        self.sound.load()
        self.sound.play()
        self.lrc.start()

    def new_title(self, title: str):
        self.title = title
        self.root.title(self.title)

    # def thread(self):
    #     # self.logger.push(UiLogger.Item(random.randint(0, 4), 'create', 'World No.%s' % random.randint(0, 9999)))
    #     if self.lrc.has_new():
    #         self.logger.push(UiLogger.Item(UiLogger.LEVEL_INFO, 'Lyric', self.lrc.next()))
    #     self.root.after(10, self.thread)

    def thread(self):
        def im_clear(x):
            if x == 255:
                return 0
            return x
        im = SpectrumMap.blend(self.spectrum_map, self.spectrum_map_wave, 1024)
        im = im.resize((256, 140))
        imp = ImageTk.PhotoImage(image=im)
        self.voice.configure(image=imp)
        self.voice.image = imp

        if self.lrc.has_new():
            self.words.push(UiLogger.Item(UiLogger.LEVEL_INFO, 'Lyric', self.lrc.next()))

        # self.root.after(1, self.thread)
        self.thread()

    def title_manager(self):
        pass

    def mainloop(self):
        self.root.mainloop()

    def gl_mainloop(self):
        self.ppt3d = PPT3D(self.ppt, window_size=(800, 600), pos=[self.root.winfo_x(), self.root.winfo_y()])
        self.ppt3d.mainloop()


if __name__ == '__main__':
    _world = World()
    _world.mainloop()
