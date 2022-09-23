import spotipy
from PIL import Image, ImageDraw, ImageFont
import base64
import constant
from io import BytesIO
from tqdm import tqdm
from diffusion import get_diffusion_image


class Cover:
    def __init__(self, sp: spotipy.Spotify):
        self.sp = sp
        self.playlists = self.sp.current_user_playlists()["items"]
        self.playlists_count = len(self.playlists)
        self.images = None
        self.pad = 500

    def generate_image(self, idx: int, low_color: int, high_color: int):
        # color_array = get_rainbow_array(self.playlists_count, low_color, high_color)
        # color = tuple(color_array[idx])

        diffusion_image = get_diffusion_image(self.get_string(idx))

        draw = ImageDraw.Draw(diffusion_image)

        font_large = ImageFont.truetype(constant.font_path, 48)
        font_small = ImageFont.truetype(constant.font_path, 24)

        draw.text((20, 0), self.playlists[idx]["name"], (255, 255, 255), font=font_large)
        draw.text((20, font_large.size + self.pad), f"Playlist: {idx + 1}/{self.playlists_count}", (255, 255, 255),
                  font=font_small)
        draw.text((20, font_large.size + font_small.size + self.pad),
                  f"Tracks: {self.playlists[idx]['tracks']['total']}", font=font_small)

        buffered = BytesIO()
        diffusion_image.save(buffered, format="JPEG")

        return buffered

    def generate_images(self, low_color: int, high_color: int):
        array = []

        # Iterate through playlists
        for idx, item in tqdm(iterable=enumerate(self.playlists)):
            array.append(self.generate_image(idx, low_color, high_color))

        self.images = array

        return array

    def set_image(self):
        array = self.images
        for idx, arr_el in tqdm(enumerate(array)):
            encoded = base64.b64encode(arr_el.getvalue())
            self.sp.playlist_upload_cover_image(self.playlists[idx]["id"], encoded)

    def get_image(self, idx: int):
        if self.images is None:
            print("No Images Generated")
        else:
            if idx >= len(self.images):
                print("Invalid Index")
            else:
                return self.images[idx]

    def get_squares(self, count: int, size: int):
        pass

    def get_string(self, idx: int):
        playlist_items = self.sp.playlist_items(self.playlists[0]['id'])['items']
        artists = []
        track_names = []
        for track in playlist_items:
            artists.append(track['track']['artists'][0]['name'])
            track_names.append(track['track']['name'])

        string = ""
        string += self.playlists[idx]["name"] + " " + str(max(set(artists), key=artists.count))

        return string
