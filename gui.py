from tkinter import *

import spotipy
from PIL import ImageTk
from PIL import Image, ImageDraw, ImageFont
from cover import Cover
from io import BytesIO
import base64


class Gui:
    def __init__(self, sp: spotipy.Spotify, width: int, height: int):
        self.root = Tk()
        self.root.resizable(False, False)

        self.width = width
        self.height = height

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack()

        self.cover = Cover(sp)

    def start(self):
        buff = self.cover.generate_image(0, 48, 209)
        img = ImageTk.PhotoImage(Image.open(buff))

        self.canvas.create_image(0, 0, anchor=NW, image=img)
        self.cover.generate_images(48, 209)

        button = Button(master=self.root, text="Apply Cover Arts", command=self.cover.set_image)
        button.pack()

        self.root.mainloop()