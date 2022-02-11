import spotipy
from spotipy.oauth2 import SpotifyOAuth
from PIL import Image, ImageDraw, ImageFont
import base64
import logging
from image import set_image

# Contains information for auth
import secret


if __name__ == "__main__":
    # Set scope
    scope = "user-library-read playlist-modify-public ugc-image-upload"

    # Authenticate
    try:
        sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                       client_id=secret.client_id,
                                                       client_secret=secret.client_secret,
                                                       redirect_uri=secret.redirect_uri))
    except:
        logging.log("Authentication Failed")

    set_image(sp)


