import os

import requests
from dotenv import load_dotenv


class SpotifyObject:
    """ Base Spotify object """
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
        """ Returns True if song is explicit, else False """
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

    @property
    def available_markets(self) -> list:
        """ Returns list of markets where track is available
            Represented by ISO 3166-1 alpha-2 codes """
        return self.raw_json["available_markets"]

    @property
    def popularity(self) -> int:
        """ Returns the popularity score of the track, from 0-100 """
        return int(self.raw_json["popularity"])


class Album(SpotifyObject):
    """ Spotify album object """

    def __init__(self, raw_json: dict):
        super().__init__(raw_json, "album")

    def __len__(self) -> int:
        """ Returns total number of tracks on the album """
        return self.raw_json["total_tracks"]

    @property
    def name(self) -> str:
        """ Returns name of album """
        return self.raw_json["name"]

    @property
    def release_date(self) -> str:
        """ Returns release date of album """
        return self.raw_json["release_date"]

    @property
    def artists(self) -> list:
        """ Returns list of all artists on the album """
        return [artist["name"] for artist in self.raw_json["artists"]]

    @property
    def album_type(self) -> str:
        """ Returns album type i.e. single, album, compilation etc. """
        return self.raw_json["album_type"]

    @property
    def tracks(self) -> list[Track]:
        """ Returns track objects for all tracks on the album """
        return [Track(item) for item in self.raw_json["tracks"]["items"]]

    @property
    def total_tracks(self) -> int:
        """ Returns the total number of tracks on the album"""
        return int(self.raw_json["total_tracks"])

    @property
    def available_markets(self) -> list:
        """ Returns list of markets where track is available
            Represented by ISO 3166-1 alpha-2 codes """
        return self.raw_json["available_markets"]

    @property
    def release_date_precision(self) -> str:
        """ Returns the precision to which the release date is known """
        return self.raw_json["release_date_precision"]

    @property
    def popularity(self) -> int:
        """ Returns the popularity score of the album, from 0-100 """
        return int(self.raw_json["popularity"])


class Artist(SpotifyObject):
    """ Spotify artist object """
    def __init__(self, raw_json: dict):
        super().__init__(raw_json, "artist")

    @property
    def name(self) -> str:
        """ Returns name of artist """
        return self.raw_json["name"]

    @property
    def total_followers(self) -> int:
        """ Returns the number of followers the artist has """
        return int(self.raw_json["followers"]["total"])

    @property
    def genres(self) -> list:
        """ Returns a list of the genres the artist is associated with """
        return self.raw_json["genres"]

    @property
    def popularity(self) -> int:
        """ Returns the popularity score of the artist, from 0-100 """
        return int(self.raw_json["popularity"])


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
        return [Album(item) for item in response["albums"]]

    def get_artists(self, artist_ids: list[str]) -> list[Artist]:
        params = {"ids": ",".join(artist_ids)}
        response = self.__send_request("artists", params)
        return [Artist(item) for item in response["artists"]["items"]]


if __name__ == "__main__":
    load_dotenv()
    connection = SpotifyConnection(os.getenv("CLIENT_ID"), os.getenv("CLIENT_SECRET"))

    tracks = connection.get_search("first class jack harlow", ["track"], 1)



    print(tracks[0].available_markets)


    # album_list = connection.get_albums(["1amYhlukNF8WdaQC3gKkgL"])
    # for track in album_list[0].tracks:
    #     if track.explicit:
    #         print("[E] ", end="")
    #     print(f"{track.name} - by {', '.join(track.artists)} ({track.minutes}:{track.seconds:02})")
