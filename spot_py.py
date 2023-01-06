class SpotifyObject:
    def __init__(self, raw_json: dict, obj_type: str):
        try:
            if raw_json["type"] == obj_type:
                self.raw_json = raw_json
            else:
                raise ValueError(f"JSON is not for a {obj_type}")
        except KeyError:
            raise ValueError("Invalid JSON")


class Track(SpotifyObject):
    """ Spotify track object """
    def __init__(self, raw_json: dict):
        super().__init__(raw_json, "track")

    def __len__(self) -> int:
        """ Returns track length in ms """
        return self.raw_json["duration_ms"]

    @property
    def name(self) -> str:
        """ Returns the name of the track """
        return self.raw_json["name"]

    @property
    def artists(self) -> list:
        """ Returns a list of all artists of the track """
        return [artist["name"] for artist in self.raw_json["artists"]]

    @property
    def explicit(self) -> bool:
        return self.raw_json["explicit"]

    @property
    def minutes(self) -> int:
        """ Returns number of minutes in track duration
            i.e. MM:ss """
        return int((len(self) / 1000) // 60)

    @property
    def seconds(self) -> int:
        """ Returns number of seconds in track duration
            i.e. mm:SS """
        return len(self) // 1000 - self.minutes * 60


class Album(SpotifyObject):
    """ Spotify album object """
    def __init__(self, raw_json: dict):
        super().__init__(raw_json, "album")

    def __len__(self) -> int:
        return self.raw_json["total_tracks"]

    @property
    def name(self) -> str:
        return self.raw_json["name"]

    @property
    def release_date(self) -> str:
        return self.raw_json["release_date"]
