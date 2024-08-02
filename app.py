import os
import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, render_template

app = Flask(__name__)

# Constants
CLIENT_ID = "7079456555d14329bfb98425a4f65306"
CLIENT_SECRET = os.getenv("SPOTIPY_CLIENT_SECRET")
SCOPE = "playlist-modify-private"
REDIRECT_URI = "http://localhost:8888/callback"


# Scrape the Billboard website and get the song names in a list
def get_songs(date, username, playlist_name):
    billboard_response = requests.get(
        f"https://www.billboard.com/charts/hot-100/{date}"
    )
    billboard_response.raise_for_status()
    soup = BeautifulSoup(billboard_response.text, "html.parser")
    return [name.get_text().strip() for name in soup.select("h3.c-title.a-no-trucate")]


# Create a private Spotify playlist on the user's account
def create_playlist(username, playlist_name, sp):
    playlist = sp.user_playlist_create(
        user=username,
        name=playlist_name,
        public=False,
        collaborative=False,
    )
    return playlist["id"]


# Search and get the Spotify URI for each song and return a list with all the URIs
def get_uris(song_names, sp, date):
    songs_uris = []
    for song_name in song_names:
        song_uri = sp.search(
            q=f"track: {song_name} year: {date.split('-')[0]}", limit=1
        )["tracks"]["items"][0]["uri"]
        print(f"Loading URI {song_uri.split(':')[2]}")
        songs_uris.append(song_uri.split(":")[2])
    return songs_uris


# Route the main homepage for the webapp with the date and username form
@app.route("/")
def home():
    return render_template("index.html")


# Route the submit page getting data from the form and run all the functions
@app.route("/submit", methods=["POST"])
def submit():
    date = request.form["date"]
    username = request.form["username"]
    playlist_name = f"{date} Billboard 100"
    song_names = get_songs(date=date, username=username, playlist_name=playlist_name)

    sp = spotipy.Spotify(
        oauth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scope=SCOPE,
            redirect_uri=REDIRECT_URI,
            username=username,
            show_dialog=True,
            open_browser=True,
            cache_path="token.txt",
        )
    )

    playlist_id = create_playlist(username=username, playlist_name=playlist_name, sp=sp)
    songs_uris = get_uris(song_names=song_names, sp=sp, date=date)
    sp.user_playlist_add_tracks(
        user=username, playlist_id=playlist_id, tracks=songs_uris
    )

    return render_template("submit.html")


if __name__ == "__main__":
    app.run(debug=True)
