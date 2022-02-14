import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageDraw, ImageFont
import base64
import constant
from color import get_rainbow_array
from io import BytesIO
from tqdm import tqdm


def set_image(sp: spotipy.Spotify):
    # Get playlist objects
    playlists = sp.current_user_playlists()
    playlist_count = len(playlists["items"])

    color_array = get_rainbow_array(playlist_count, 48, 209)

    # Iterate through playlists
    for idx, item in tqdm(iterable=enumerate(playlists["items"])):
        item_id = item["id"]
        color = tuple(color_array[idx])
        img = Image.new('RGB', (constant.png_px_size, constant.png_px_size), color=color)

        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype(constant.font_path, 64)
        draw.text((20, 10), item["name"], (255, 253, 247), font=font)

        buffered = BytesIO()
        img.save(buffered, format="JPEG")

        encoded = base64.b64encode(buffered.getvalue())
        sp.playlist_upload_cover_image(item_id, encoded)
