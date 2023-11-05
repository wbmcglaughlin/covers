import spotipy
from PIL import Image, ImageDraw, ImageFont
import base64
import constant
from io import BytesIO
from tqdm import tqdm


class Cover:
    def __init__(self, sp: spotipy.Spotify):
        self.sp = sp
        self.playlists = self.sp.current_user_playlists()["items"]
        self.playlists_count = len(self.playlists)
        self.images = None
        self.pad = 500

    def generate_image(self, string: str, idx: int):
        """
        :param string:
        :param idx:
        """
        image = get_image(string)

        draw = ImageDraw.Draw(image)

        font_large = ImageFont.truetype(constant.font_path, 48)
        font_small = ImageFont.truetype(constant.font_path, 24)

        draw.text((20, 0), self.playlists[idx]["name"], (255, 255, 255), font=font_large)
        draw.text(
            (20, font_large.size + self.pad), 
            f"Playlist: {idx + 1}/{self.playlists_count}", (255, 255, 255),
            font=font_small
        )
        draw.text(
            (20, font_large.size + font_small.size + self.pad),
            f"Tracks: {self.playlists[idx]['tracks']['total']}", 
            font=font_small
        )

        buffered = BytesIO()
        image.save(buffered, format="JPEG")

        return buffered

    def set_image(self):
        """
        
        """
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
        """
        :param idx:
        """
        playlist_items = self.sp.playlist_items(self.playlists[idx]['id'])['items']
        artists = []
        track_names = []
        for track in playlist_items:
            artists.append(track['track']['artists'][0]['name'])
            track_names.append(track['track']['name'])

        string = ""
        string += str(max(set(artists), key=artists.count)) + " " + self.playlists[idx]["name"]
        print(string)

        return string
