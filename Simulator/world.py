from tkinter import *
from Simulator.Lyric.lyric import *
from Simulator.Me import *
from Simulator.Render import *
from Simulator.Sound.sound import *
from Simulator.ui_logger import UiLogger
import random


class World:
    def __init__(self, root=None):
        self.root = root
        if self.root is None:
            self.root = Tk()

        self.title = 'World Simulator'
        self.new_title(self.title)

        self.logger = UiLogger(self.root, max_height=25, simplify=True)
        self.logger.logger().pack(fill=BOTH, expand=0)

        self.lrc = Lyric()

        Sound.load()
        Sound.play()
        self.lrc.start()

        self.thread()

    def new_title(self, title: str):
        self.title = title
        self.root.title(self.title)

    def thread(self):
        # self.logger.push(UiLogger.Item(random.randint(0, 4), 'create', 'World No.%s' % random.randint(0, 9999)))
        if self.lrc.has_new():
            self.logger.push(UiLogger.Item(UiLogger.LEVEL_INFO, 'Lyric', self.lrc.next()))
        self.root.after(10, self.thread)

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    _world = World()
    _world.mainloop()
