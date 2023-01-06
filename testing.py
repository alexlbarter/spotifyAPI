import os
import requests
import spot_py
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

# auth_response = requests.post("https://accounts.spotify.com/api/token", {
#     "grant_type": "client_credentials",
#     "client_id": client_id,
#     "client_secret": client_secret
# })
#
# access_token = auth_response.json()["access_token"]
# headers = {"Authorization": f"Bearer {access_token}"}

connection = spot_py.SpotifyConnection(client_id, client_secret)


search_term = input("Enter search term: ")
# search_type = input("Search type: ")

# params = {"type": search_type, "limit": 5, "q": search_term}
#
# response = requests.get(f"https://api.spotify.com/v1/search", headers=headers, params=params)
# response_json = response.json()

response = connection.get_search(search_term, ["track", "album", "artist"])

count = 1
for item in response:
    if item.type == "track":
        print(f"{count}) {item.name} - by {', '.join(item.artists)}", end="")
        if item.explicit:
            print(" [E]", end="")
        print(f" ({item.minutes}:{item.seconds:02})")
        count += 1
    elif item.type == "album":
        print(f"{item.name}, {len(item)} tracks")

