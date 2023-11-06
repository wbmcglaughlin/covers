import os.path
import logging
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from src.gui import Gui
from src.configurations import init_configurations, get_persistent_data_path

# Contains information for auth
import src.secret as secret

if __name__ == "__main__":
    persistent_data_path = get_persistent_data_path()

    if os.path.exists(persistent_data_path / "Covers"):
        for pth in os.listdir(persistent_data_path / "Covers"):
            if pth[-3:] == "png":
                os.remove(persistent_data_path / "Covers" / pth)
    else:
        os.mkdir(persistent_data_path / "Covers")

    init_configurations()

    # Set scope
    SCOPE = "user-library-read playlist-modify-public ugc-image-upload"

    # Authenticate
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SCOPE,
                                                       client_id=secret.client_id,
                                                       client_secret=secret.client_secret,
                                                       redirect_uri=secret.redirect_uri))
        gui = Gui(sp, 420, 420)
        gui.start()

    except spotipy.SpotifyException as e:
        logging.log("Authentication Failed")
