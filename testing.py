import os
import requests
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

header = {"Authorization": f"Bearer {access_token}"}
response = requests.get("https://api.spotify.com/v1/tracks/1eprzC29mwUQqcVj0eILdx", headers=header)

for artist in response.json()["artists"]:
    print(artist["name"])
