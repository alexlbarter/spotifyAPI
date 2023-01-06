import requests


class SpotifyObject:
    def __init__(self, raw_json: dict, obj_type: str):
        try:
            if raw_json["type"] == obj_type:
                self.raw_json = raw_json
                self.type = obj_type
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


class Artist(SpotifyObject):
    def __init__(self, raw_json: dict):
        super().__init__(raw_json, "artist")


class SpotifyConnection:
    def __init__(self, client_id: str, client_secret: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self.__get_access_token()
        self.headers = {"Authorization": f"Bearer {self.access_token}"}
        self.api_endpoint = "https://api.spotify.com/v1"
        self.obj_handlers = {"track": Track,
                             "album": Album,
                             "artist": Artist}

    def __get_access_token(self) -> str:
        auth_response = requests.post("https://accounts.spotify.com/api/token", {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret
        })
        return auth_response.json()["access_token"]

    def __send_request(self, request_type: str, params: dict) -> dict:
        response = requests.get(f"{self.api_endpoint}/{request_type}", headers=self.headers, params=params)
        if response.ok:
            return response.json()
        else:
            response.raise_for_status()

    def get_search(self, query: str, search_types: list[str], limit=10) -> list:
        params = {"q": query, "type": ",".join(search_types), "limit": limit}
        response = self.__send_request("search", params)
        results = []
        for item_type in response:
            for item in response[item_type]["items"]:
                results.append(self.obj_handlers[item["type"]].__call__(item))
        return results

    def get_tracks(self, track_ids: list[str]) -> list[Track]:
        params = {"ids": ",".join(track_ids)}
        response = self.__send_request("tracks", params)
        return [Track(item) for item in response["tracks"]["items"]]

    def get_albums(self, album_ids: list[str]) -> list[Album]:
        params = {"ids": ",".join(album_ids)}
        response = self.__send_request("albums", params)
        return [Album(item) for item in response["albums"]["items"]]

    def get_artists(self, artist_ids: list[str]) -> list[Artist]:
        params = {"ids": ",".join(artist_ids)}
        response = self.__send_request("artists", params)
        return [Artist(item) for item in response["artists"]["items"]]
