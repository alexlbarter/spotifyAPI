import os
import requests
import spot_py
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

auth_response = requests.post("https://accounts.spotify.com/api/token", {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
})

access_token = auth_response.json()["access_token"]
headers = {"Authorization": f"Bearer {access_token}"}


search_term = input("Enter search term: ")
search_type = input("Search type: ")

params = {"type": search_type, "limit": 5, "q": search_term}

response = requests.get(f"https://api.spotify.com/v1/search", headers=headers, params=params)
response_json = response.json()

count = 1
for item in response_json[search_type + "s"]["items"]:
    if search_type == "track":
        track = spot_py.Track(item)
        print(f"{count}) {track.name} - by {', '.join(track.artists)}", end="")
        if track.explicit:
            print(" [E]", end="")
        print(f" ({track.minutes}:{track.seconds:02})")
        count += 1
    elif search_type == "album":
        album = spot_py.Album(item)
        print(f"{album.name}, {len(album)} tracks")

