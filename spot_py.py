import requests


class SpotifyConnection:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.__get_access_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.api_endpoint = "https://api.spotify.com/v1"

    def __get_access_token(self) -> str:
        auth_response = requests.post("https://accounts.spotify.com/api/token", {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        })
        return auth_response.json()["access_token"]

    def get_search(self, query: str, search_types: list[str], limit=10) -> dict:
        params = {"q": query, "type": ",".join(search_types), "limit": limit}
        return requests.get(f"{self.api_endpoint}/search", headers=self.headers, params=params).json()

    def get_tracks(self, track_ids: list[str]) -> dict:
        id_str = ",".join(track_ids)
        return requests.get(f"{self.api_endpoint}/tracks", headers=self.headers, params={"ids": id_str}).json()

    def get_artists(self, artist_ids: list[str]) -> dict:
        id_str = ",".join(artist_ids)
        return requests.get(f"{self.api_endpoint}/artists", headers=self.headers, params={"ids": id_str}).json()


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
