import os.path
import tkinter
from tkinter import *

import spotipy
import urllib.request
from PIL import ImageTk
from PIL import Image, ImageDraw, ImageFont
from cover import Cover
from io import BytesIO
import base64

COVER_FILE_PATH = "./Covers"


class Gui:
    def __init__(self, sp: spotipy.Spotify, width: int, height: int):
        if not os.path.exists(COVER_FILE_PATH):
            os.mkdir(COVER_FILE_PATH)

        self.root = Tk()
        self.root.resizable(False, False)

        self.width = width
        self.height = height
        self.generated_cover = None

        self.canvas = Canvas(self.root, width=self.width, height=self.height)
        self.canvas.pack(fill='both', expand=1)

        self.current_cover = None

        self.sp = sp
        self.cover = Cover(sp)
        self.index_val = 0
        self.index = StringVar()

    def start(self):
        self.get_current_playlist_cover()

        left_button = Button(master=self.root, text="<<", command=self.decrement_index)
        left_button.pack(side=LEFT)

        button = Button(master=self.root, text="Generate Cover", command=self.generate_image)
        button.pack(side=LEFT)

        button = Button(master=self.root, text="Apply Cover Art", command=self.apply_generated_cover)
        button.pack(side=LEFT)

        right_button = Button(master=self.root, text=">>", command=self.increment_index)
        right_button.pack(side=LEFT)

        text = Label(self.root, textvariable=self.index)
        text.pack()

        self.root.mainloop()

    def get_current_playlist_cover(self):
        if not os.path.exists(f'{COVER_FILE_PATH}/cover_{self.index_val}.png'):
            spotify_cover_image = self.sp.playlist_cover_image(
                self.sp.current_user_playlists()["items"][self.index_val]["id"])[0]['url']
            urllib.request.urlretrieve(spotify_cover_image, f'{COVER_FILE_PATH}/cover_{self.index_val}.png')

        img = ImageTk.PhotoImage(Image.open(f'{COVER_FILE_PATH}/cover_{self.index_val}.png'))
        self.current_cover = tkinter.Label(image=img)
        self.current_cover.image = img
        self.current_cover.place(x=0, y=0)

    def decrement_index(self):
        self.index_val -= 1
        self.index_val = max(self.index_val, 0)
        self.index.set(str(self.index_val))
        self.generated_cover = None
        self.get_current_playlist_cover()

    def increment_index(self):
        self.index_val += 1
        self.index.set(str(self.index_val))
        self.generated_cover = None
        self.get_current_playlist_cover()

    def get_image(self):
        self.cover.get_image(self.index_val)

    def generate_image(self):
        buff = self.cover.generate_image(self.index_val)
        img = ImageTk.PhotoImage(Image.open(buff))
        self.current_cover = tkinter.Label(image=img)
        self.current_cover.image = img
        self.current_cover.place(x=0, y=0)
        self.generated_cover = buff

    def apply_generated_cover(self):
        if self.generated_cover is not None:
            encoded = base64.b64encode(self.generated_cover.getvalue())
            self.sp.playlist_upload_cover_image(
                self.sp.current_user_playlists()["items"][self.index_val]["id"],
                encoded
            )

