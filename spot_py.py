def get_track_name(track_json: dict) -> str:
    """ Returns name of track when passed in track item dict """
    return track_json["name"]


def get_artists(track_json: dict) -> list:
    """ Returns list of artists when passed in track item dict """
    artist_list = []
    for artist in track_json["artists"]:
        artist_list.append(artist["name"])
    return artist_list
