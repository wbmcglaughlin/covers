import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageDraw, ImageFont
import base64
import constant
from color import get_rainbow_array


def set_image(sp: spotipy.Spotify):
    # Get playlist objects
    playlists = sp.current_user_playlists()
    playlist_count = len(playlists["items"])

    color_array = get_rainbow_array(playlist_count, 48, 209)

    # Iterate through playlists
    for idx, item in enumerate(playlists["items"]):
        item_id = item["id"]
        color = tuple(color_array[idx])
        img = Image.new('RGB', (constant.png_px_size, constant.png_px_size), color=color)
        img.save(f'./cover_art/{idx}.png')
        encoded = base64.b64encode(open(f'./cover_art/{idx}.png', 'rb').read())
        sp.playlist_upload_cover_image(item_id, encoded)
        print(f"Playlist [ {item['name']} ] cover art changed with color"
              f" {color}")
