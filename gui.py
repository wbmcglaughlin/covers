from tkinter import *

import spotipy
from PIL import ImageTk
from image import Image


class Gui:
    def __init__(self, sp: spotipy.Spotify, width: int, height: int):
        self.root = Tk()
        self.root.resizable(False, False)

        self.width = width
        self.height = height

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.image = Image(sp)

    def start(self):
        img = self.image.get_image(0)
        self.root.mainloop()