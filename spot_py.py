class Track:
    def __init__(self, raw_json: dict):
        self.raw_json = raw_json

    @property
    def track_name(self) -> str:
        """ Returns the name of the track """
        return self.raw_json["name"]

    @property
    def artists(self) -> list:
        """ Returns a list of all artists of the track """
        return [artist["name"] for artist in self.raw_json["artists"]]


