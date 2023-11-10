import os.path
import base64
import pathlib
import urllib.request
import tkinter as tk
from tkinter import filedialog
from io import BytesIO
from PIL import ImageTk
from PIL import Image, ImageDraw, ImageFont
import spotipy

from src.data import get_playlist_titles, get_playlist_items
from src.configurations import get_persistent_data_path
from src.cover import Cover
from src.constant import font_path


class Gui:
    """
    Application GUI.
    """

    def __init__(self, sp: spotipy.Spotify, width: int, height: int):
        """
        :param sp: (spotipy.Spotify) spotify class.
        :param width: (int) width of gui window.
        :param height: (int) height of gui window.
        """
        self.config_path = get_persistent_data_path() / "Covers"
        if not os.path.exists(self.config_path):
            os.mkdir(self.config_path)

        self.root = tk.Tk()
        self.sp = sp
        self.cover = Cover(sp)

        self.width = width
        self.height = height
        self.generated_cover_img = None
        self.generated_cover_bytes = None
        self.canvas = tk.Frame(self.root)

        self.current_cover = None
        self.input_canvas = tk.Frame(self.root)
        self.input_canvas.grid(row=0, column=1)

        playlist_gen_string_text = tk.Label(
            master=self.input_canvas, text="Playlist Generator Input String")
        playlist_gen_string_text.grid(row=2, column=0)
        self.playlist_string_text = tk.Text(master=self.input_canvas)
        self.playlist_string_text.grid(row=3)

        options = get_playlist_titles(self.sp)
        self.playlist_selection_name = tk.StringVar(self.input_canvas)
        self.playlist_selection_name.set(options[0])  # default value
        self.playlist_selection_name.trace_variable(
            "w", self.change_to_playlist)
        playlist_choice_string_text = tk.Label(
            master=self.input_canvas, text="Playlist Selection")
        playlist_choice_string_text.grid(row=0, column=0)
        self.dropdown = tk.OptionMenu(
            self.input_canvas, self.playlist_selection_name, *options)
        self.dropdown.grid(row=1)

        self.index_val = 0
        self.index = tk.StringVar()

    def start(self):
        """
        Start the program.
        """
        self.get_current_playlist_cover()

        # Menu Button Selection Options
        left_button = tk.Button(
            master=self.canvas,
            text="<<",
            command=self.decrement_index
        )
        left_button.grid(row=0, column=0)

        import_phtoto_button = tk.Button(
            master=self.canvas,
            text="Import Photo",
            command=self.open_image_selector
        )
        import_phtoto_button.grid(row=0, column=1)

        button = tk.Button(
            master=self.canvas,
            text="Generate Cover",
            command=self.generate_image
        )
        button.grid(row=0, column=2)

        border_button = tk.Button(
            master=self.canvas,
            text="Add Border",
            command=self.add_title
        )
        border_button.grid(row=0, column=5)

        button = tk.Button(
            master=self.canvas,
            text="Apply Cover Art",
            command=self.apply_generated_cover
        )
        button.grid(row=0, column=3)

        right_button = tk.Button(
            master=self.canvas,
            text=">>",
            command=self.increment_index
        )
        right_button.grid(row=0, column=6)

        rotate_button = tk.Button(
            master=self.canvas,
            text="r",
            command=self.rotate
        )
        rotate_button.grid(row=0, column=7)

        text = tk.Label(self.root, textvariable=self.index)
        text.grid(row=0, column=8)

        self.canvas.grid(row=1, column=1)
        self.root.mainloop()

    def open_image_selector(self):
        """_summary_
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.gif *.bmp *.ppm")])
        if file_path:
            image = Image.open(file_path)
            self.apply_image(image)

    def get_current_playlist_cover(self):
        """
        Get current playlists cover.
        """
        if not os.path.exists(f'{self.config_path}/cover_{self.index_val}.png'):
            spotify_cover_image = self.sp.playlist_cover_image(
                get_playlist_items(self.sp)[self.index_val]["id"])[0]['url']
            urllib.request.urlretrieve(
                spotify_cover_image, f'{self.config_path}/cover_{self.index_val}.png')

        try:
            image_path = pathlib.Path(
                f'{self.config_path}/cover_{self.index_val}.png')
            print(image_path)
            img_pil = Image.open(image_path)
            img_pil = img_pil.resize((self.width, self.height), Image.BICUBIC)
            img = ImageTk.PhotoImage(img_pil)
        except Exception as e:
            print(e)
            exit()

        self.current_cover = tk.Label(
            master=self.root, image=img, height=self.height, width=self.width)
        self.current_cover.image = img
        self.current_cover.place(x=0, y=0)
        self.current_cover.grid(row=0, column=0)

    def decrement_index(self):
        """
        Decrement index.
        """
        self.index_val -= 1
        self.index_val = max(self.index_val, 0)
        self.on_playlist_change()

    def increment_index(self):
        """
        Increment index.
        """
        self.index_val += 1
        self.on_playlist_change()

    def rotate(self):
        """
        Rotate the current image by 90 degrees.
        """
        rotated_image = self.generated_cover_img.rotate(90)
        self.apply_image(rotated_image)

    def on_playlist_change(self):
        """
        Run on playlist change.
        """
        self.index.set(str(self.index_val))
        self.generated_cover_bytes = None

        string = self.cover.get_string(self.index_val)
        self.playlist_string_text.delete(1.0, "end")
        self.playlist_string_text.insert(1.0, string)
        self.get_current_playlist_cover()

    def change_to_playlist(self, *args):
        """
        Change to selected playlist.
        """
        playlist = self.playlist_selection_name.get()
        playlists = get_playlist_titles(self.sp)
        self.index_val = playlists.index(playlist)
        self.on_playlist_change()

    def get_image(self):
        self.cover.get_image(self.index_val)

    def generate_image(self):
        buff = self.cover.generate_image(
            self.playlist_string_text.get(1.0, "end"), self.index_val)
        img_pil = Image.open(buff)

        self.apply_image(img_pil)

    def apply_image(self, image):
        """
        Apply a new image to the class attributes.
        """
        img_pil = self.crop_image_to_square(image)
        img_pil = img_pil.resize((self.width, self.height), Image.NEAREST)
        img = ImageTk.PhotoImage(img_pil)

        self.current_cover = tk.Label(image=img)
        self.current_cover.image = img
        self.current_cover.place(x=0, y=0)
        self.current_cover.grid(row=0, column=0)

        buffer = BytesIO()
        img_pil.save(buffer, format="JPEG")
        img_bytes = buffer.getvalue()
        buffer.close()

        self.generated_cover_img = img_pil
        self.generated_cover_bytes = img_bytes

    def add_title(self):
        """
        Add a title to the image.
        """
        font_small = ImageFont.truetype(font_path, 44)
        draw = ImageDraw.Draw(self.generated_cover_img)

        title = get_playlist_items(self.sp)[self.index_val]["name"]

        draw.text((8, -4), title, fill=(120, 120, 120), font=font_small)
        draw.text((10, -2), title, fill=(255, 255, 255), font=font_small)
        self.apply_image(self.generated_cover_img)

    def crop_image_to_square(self, image):
        """
        Center crop image to a square.
        """
        width, height = image.size
        min_dim = min(width, height)
        left = (width - min_dim) / 2
        top = (height - min_dim) / 2
        right = (width + min_dim) / 2
        bottom = (height + min_dim) / 2

        return image.crop((left, top, right, bottom))

    def apply_generated_cover(self):
        """
        Apply generated cover to spotify by encoding to bytes.
        """
        if self.generated_cover_bytes is not None:
            encoded = base64.b64encode(self.generated_cover_bytes)
            self.sp.playlist_upload_cover_image(
                self.sp.current_user_playlists(
                )["items"][self.index_val]["id"],
                encoded
            )
