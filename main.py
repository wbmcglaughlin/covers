import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
from gui import Gui
from huggingface_hub import notebook_login
import torch
import constant

# Contains information for auth
import secret

if __name__ == "__main__":
    notebook_login()
    print(torch.cuda.is_available())
    print(torch.cuda.memory_summary(device=None, abbreviated=False))
    # Set scope
    scope = "user-library-read playlist-modify-public ugc-image-upload"

    # Authenticate
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                       client_id=secret.client_id,
                                                       client_secret=secret.client_secret,
                                                       redirect_uri=secret.redirect_uri))
    except spotipy.SpotifyException as e:
        logging.log("Authentication Failed")

    gui = Gui(sp, constant.png_px_size, constant.png_px_size)
    gui.start()
