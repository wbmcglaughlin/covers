import spotipy
from PIL import Image, ImageDraw, ImageFont
import base64
import constant
from color import get_rainbow_array
from io import BytesIO
from tqdm import tqdm


class Image:
    def __init__(self, sp: spotipy.Spotify):
        self.sp = sp
        self.images = None

    def generate_image(self, idx: int):
        pass

    def generate_images(self, low_color: int, high_color: int):
        # Get playlist objects
        playlists = self.sp.current_user_playlists()
        playlist_count = len(playlists["items"])

        color_array = get_rainbow_array(playlist_count, low_color, high_color)
        array = []

        # Iterate through playlists
        for idx, item in tqdm(iterable=enumerate(playlists["items"])):
            color = tuple(color_array[idx])
            img = Image.new('RGB', (constant.png_px_size, constant.png_px_size), color=color)

            draw = ImageDraw.Draw(img)
            # draw.rectangle((10, 10, 20, 20), fill=(0, 0, 0))

            font_large = ImageFont.truetype(constant.font_path, 64)
            font_small = ImageFont.truetype(constant.font_path, 50)

            draw.text((20, 0), item["name"], (255, 255, 255), font=font_large)
            draw.text((20, 560), f"Playlist: {idx + 1}/{playlist_count}", (255, 255, 255), font=font_small)

            buffered = BytesIO()
            img.save(buffered, format="JPEG")

            array.append(buffered)

        self.images = array

        return array

    def set_image(self):
        array = self.generate_images(48, 209)
        playlists = self.sp.current_user_playlists()
        for idx, arr_el in tqdm(enumerate(array)):
            encoded = base64.b64encode(arr_el.getvalue())
            self.sp.playlist_upload_cover_image(playlists[idx]["id"], encoded)

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
