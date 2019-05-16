from tkinter import *
from Simulator.Lyric import *
from Simulator.Me import *
from Simulator.Render import *
from Simulator.Lyric import *


class World:
    def __init__(self, root=None):
        self.root = root
        if self.root is None:
            self.root = Tk()

        self.title = 'World Simulator'
        self.new_title(self.title)

    def new_title(self, title: str):
        self.title = title
        self.root.title(self.title)

    def mainloop(self):
        self.root.mainloop()


if __name__ == '__main__':
    _world = World()
    _world.mainloop()
