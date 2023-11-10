import spotipy


LIMIT = 50


def get_playlist_titles(sp: spotipy.Spotify):
    """
    Get list of playlist titles.
    """
    titles = []
    offset = 0
    while True:
        playlists = sp.current_user_playlists(
            offset=offset, limit=LIMIT)["items"]
        for playlist in playlists:
            titles.append(playlist["name"])

        if len(playlists) < 50:
            break

        offset += 50

    return titles


def get_playlist_items(sp: spotipy.Spotify):
    """
    Get list of playlist titles.
    """
    titles = []
    offset = 0
    while True:
        playlists = sp.current_user_playlists(
            offset=offset, limit=LIMIT)["items"]
        for playlist in playlists:
            titles.append(playlist)

        if len(playlists) < 50:
            break

        offset += 50

    return titles
