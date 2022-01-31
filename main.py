import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageDraw, ImageFont
import base64
import secret

scope = "user-library-read playlist-modify-public ugc-image-upload"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                               client_id=secret.client_id,
                                               client_secret=secret.client_secret,
                                               redirect_uri=secret.redirect_uri))

playlists = sp.current_user_playlists()
playlist_count = len(playlists["items"])

for idx, item in enumerate(playlists["items"]):
    item_id = item["id"]
    color = (int(255 * idx / playlist_count), 255, 235)
    img = Image.new('RGB', (640, 640), color=color)
    img.save(f'./cover_art/{idx}.png')
    encoded = base64.b64encode(open(f'./cover_art/{idx}.png', 'rb').read())
    sp.playlist_upload_cover_image(item_id, encoded)
    print(f"Playlist [ {item['name']} ] cover art changed with color"
          f" {color}")
