import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth

# Constants
CLIENT_ID = "7079456555d14329bfb98425a4f65306"
CLIENT_SECRET = "366ab3afe1f8448f80d0c8176a111c56"
SCOPE = "playlist-modify-private"
REDIRECT_URI = "https://example.com"

# Ask for the desired date, and for user's Spotify User ID
requested_date = input(
    "Which day do you want to travel to? Type the date in the YYYY-MM-DD format: "
)
spotify_user_id = input("What's your Spotify user ID/username?: ")

# Write the name of the playlist
playlist_name = f"{requested_date} Billboard 100"

# Access the Billboard website with the desired date
billboard_response = requests.get(
    f"https://www.billboard.com/charts/hot-100/{requested_date}"
)
billboard_response.raise_for_status()

# Put all the song names in the page in a list
soup = BeautifulSoup(billboard_response.text, "html.parser")
song_names = [
    name.get_text().strip() for name in soup.select("h3.c-title.a-no-trucate")
]

# Initiates the Spotify and SpotifyOAuth classes
sp = spotipy.Spotify(
    oauth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        scope=SCOPE,
        redirect_uri=REDIRECT_URI,
        username=spotify_user_id,
        show_dialog=True,
        cache_path="token.txt",
    )
)

# Creates a private playlist on Spotify using the user's info
playlist = sp.user_playlist_create(
    user=spotify_user_id,
    name=playlist_name,
    public=False,
    collaborative=False,
)
playlist_id = playlist["id"]

# Loop through all the song names, get their URIs, and append them to a list
songs_uris = []
for name in song_names:
    song_uri = sp.search(q=f"track: {name} year: {requested_date.split('-')[0]}", limit=1)["tracks"]["items"][0]["uri"]
    print(f"Loading URI {song_uri.split(":")[2]}")
    songs_uris.append(song_uri.split(":")[2])

# Add the tracks from their URIs to the previous playlist
sp.user_playlist_add_tracks(
    user=spotify_user_id, playlist_id=playlist_id, tracks=songs_uris
)
