import os.path
import tkinter
from tkinter import *

import spotipy
import urllib.request
from PIL import ImageTk
from PIL import Image
from cover import Cover
import base64

COVER_FILE_PATH = "./Covers"


class Gui:
    def __init__(self, sp: spotipy.Spotify, width: int, height: int):
        if not os.path.exists(COVER_FILE_PATH):
            os.mkdir(COVER_FILE_PATH)

        self.root = Tk()
        self.sp = sp
        self.cover = Cover(sp)

        self.width = width
        self.height = height
        self.generated_cover = None

        self.canvas = Frame(self.root)

        self.current_cover = None
        self.input_canvas = Frame(self.root)
        self.input_canvas.grid(row=0, column=1)

        playlist_gen_string_text = Label(master=self.input_canvas, text="Playlist Generator Input String")
        playlist_gen_string_text.grid(row=2, column=0)
        self.playlist_string_text = Text(master=self.input_canvas)
        self.playlist_string_text.grid(row=3)

        options = self.get_playlist_titles()
        self.playlist_selection_name = StringVar(self.input_canvas)
        self.playlist_selection_name.set(options[0])  # default value
        self.playlist_selection_name.trace_variable("w", self.change_to_playlist)
        playlist_choice_string_text = Label(master=self.input_canvas, text="Playlist Selection")
        playlist_choice_string_text.grid(row=0, column=0)
        self.dropdown = OptionMenu(self.input_canvas, self.playlist_selection_name, *options)
        self.dropdown.grid(row=1)

        self.index_val = 0
        self.index = StringVar()

    def start(self):
        self.get_current_playlist_cover()

        # Menu Button Selection Options
        left_button = Button(master=self.canvas, text="<<", command=self.decrement_index)
        left_button.grid(row=0, column=0)

        button = Button(master=self.canvas, text="Generate Cover", command=self.generate_image)
        button.grid(row=0, column=1)

        button = Button(master=self.canvas, text="Apply Cover Art", command=self.apply_generated_cover)
        button.grid(row=0, column=2)

        right_button = Button(master=self.canvas, text=">>", command=self.increment_index)
        right_button.grid(row=0, column=3)

        text = Label(self.root, textvariable=self.index)
        text.grid(row=0, column=4)

        self.canvas.grid(row=1, column=1)
        self.root.mainloop()

    def get_current_playlist_cover(self):
        if not os.path.exists(f'{COVER_FILE_PATH}/cover_{self.index_val}.png'):
            spotify_cover_image = self.sp.playlist_cover_image(
                self.sp.current_user_playlists()["items"][self.index_val]["id"])[0]['url']
            urllib.request.urlretrieve(spotify_cover_image, f'{COVER_FILE_PATH}/cover_{self.index_val}.png')

        img_pil = Image.open(f'{COVER_FILE_PATH}/cover_{self.index_val}.png')
        img_pil = img_pil.resize((self.width, self.height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img_pil)

        self.current_cover = tkinter.Label(master=self.root, image=img, height=self.height, width=self.width)
        self.current_cover.image = img
        self.current_cover.place(x=0, y=0)
        self.current_cover.grid(row=0, column=0)

    def get_playlist_titles(self):
        titles = []
        for playlist in self.sp.current_user_playlists()["items"]:
            titles.append(playlist["name"])

        return titles

    def decrement_index(self):
        self.index_val -= 1
        self.index_val = max(self.index_val, 0)
        self.on_playlist_change()

    def increment_index(self):
        self.index_val += 1
        self.on_playlist_change()

    def on_playlist_change(self):
        self.index.set(str(self.index_val))
        self.generated_cover = None

        string = self.cover.get_string(self.index_val)
        self.playlist_string_text.delete(1.0, "end")
        self.playlist_string_text.insert(1.0, string)
        self.get_current_playlist_cover()

    def change_to_playlist(self, *args):
        playlist = self.playlist_selection_name.get()
        playlists = self.get_playlist_titles()
        self.index_val = playlists.index(playlist)
        self.on_playlist_change()

    def get_image(self):
        self.cover.get_image(self.index_val)

    def generate_image(self):
        buff = self.cover.generate_image(self.playlist_string_text.get(1.0, "end"), self.index_val)

        img_pil = Image.open(buff)
        img_pil = img_pil.resize((self.width, self.height), Image.ANTIALIAS)
        img = ImageTk.PhotoImage(img_pil)

        self.current_cover = tkinter.Label(image=img)
        self.current_cover.image = img
        self.current_cover.place(x=0, y=0)
        self.current_cover.grid(row=0, column=0)
        self.generated_cover = buff

    def apply_generated_cover(self):
        if self.generated_cover is not None:
            encoded = base64.b64encode(self.generated_cover.getvalue())
            self.sp.playlist_upload_cover_image(
                self.sp.current_user_playlists()["items"][self.index_val]["id"],
                encoded
            )

