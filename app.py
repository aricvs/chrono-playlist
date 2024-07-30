import requests
import spotipy
from bs4 import BeautifulSoup
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, render_template

app = Flask(__name__)

# Constants
# TODO remove the need to put the redirect URI in the terminal
CLIENT_ID = "7079456555d14329bfb98425a4f65306"
CLIENT_SECRET = "366ab3afe1f8448f80d0c8176a111c56"
SCOPE = "playlist-modify-private"
REDIRECT_URI = "https://example.com"

def get_songs(date, username, playlist_name):
    billboard_response = requests.get(
        f"https://www.billboard.com/charts/hot-100/{date}"
    )
    billboard_response.raise_for_status()

    soup = BeautifulSoup(billboard_response.text, "html.parser")
    song_names = [
        name.get_text().strip() for name in soup.select("h3.c-title.a-no-trucate")
    ]
    return song_names

@app.route("/")
def root():
    return render_template("index.html")


# TODO separate into functions instead of one big spaghetti
@app.route("/submit", methods=["POST"])
def submit():
    date = request.form["date"]
    username = request.form["username"]
    playlist_name = f"{date} Billboard 100"

    song_names = get_songs(date=date, username=username, playlist_name=playlist_name)
    print(song_names)

    sp = spotipy.Spotify(
        oauth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            scope=SCOPE,
            redirect_uri=REDIRECT_URI,
            username=username,
            show_dialog=True,
            cache_path="token.txt",
        )
    )

    playlist = sp.user_playlist_create(
        user=username,
        name=playlist_name,
        public=False,
        collaborative=False,
    )
    playlist_id = playlist["id"]

    songs_uris = []
    for song_name in song_names:
        song_uri = sp.search(q=f"track: {song_name} year: {date.split('-')[0]}", limit=1)["tracks"]["items"][0]["uri"]
        print(f"Loading URI {song_uri.split(":")[2]}")
        songs_uris.append(song_uri.split(":")[2])

    sp.user_playlist_add_tracks(
        user=username, playlist_id=playlist_id, tracks=songs_uris
    )
    
    return "Success"


if __name__ == "__main__":
    app.run(debug=True)
