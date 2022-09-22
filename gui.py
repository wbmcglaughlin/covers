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
        self.canvas.pack(fill='both', expand=1)

        self.cover = Cover(sp)
        self.index_val = 0
        self.index = StringVar()

    def start(self):
        buff = self.cover.generate_image(0, 48, 209)
        img = ImageTk.PhotoImage(Image.open(buff))

        self.canvas.create_image(0, 0, anchor=NW, image=img)

        left_button = Button(master=self.root, text="<<", command=self.decrement_index)
        left_button.pack()
        button = Button(master=self.root, text="Apply Cover Arts", command=self.cover.set_image)
        button.pack()
        right_button = Button(master=self.root, text=">>", command=self.increment_index)
        right_button.pack()
        text = Label(self.root, textvariable=self.index)
        text.pack()
        self.root.mainloop()

    def decrement_index(self):
        self.index_val -= 1
        self.index_val = max(self.index_val, 0)
        self.index.set(str(self.index_val))

    def increment_index(self):
        self.index_val += 1
        self.index.set(str(self.index_val))

    def get_image(self):
        self.cover.get_image(self.index_val)