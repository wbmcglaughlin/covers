import os.path

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging
from gui import Gui

# Contains information for auth
import secret

if __name__ == "__main__":
    if os.path.exists("./Covers"):
        for pth in os.listdir("./Covers"):
            if pth[-3:] == "png":
                os.remove("./Covers/" + pth)

    # Set scope
    scope = "user-library-read playlist-modify-public ugc-image-upload"

    # Authenticate
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                       client_id=secret.client_id,
                                                       client_secret=secret.client_secret,
                                                       redirect_uri=secret.redirect_uri))
        gui = Gui(sp, 420, 420)
        gui.start()

    except spotipy.SpotifyException as e:
        logging.log("Authentication Failed")


