# chrono-playlist

A Flask webapp that gets a user's Spotify user ID and a specific date, then creates a playlist based on the Billboard's top 100 from that date on their Spotify account.

Usage: pick a date from the picker, paste your Spotify username on the required field, and click submit. An authentication prompt will pop up in your browser so that you can login to your Spotify account and authorize the app. Once you authenticate, the webapp will take a couple of moments to load the next page while the songs are being searched and added on the backend, just wait for a couple of moments and you will be redirected to a success page. This means that the playlist was created successfully.

This makes use of Spotify API and the Spotipy library in order to make changes on a Spotify account. It scrapes Bilbboard's website: https://www.billboard.com/charts/hot-100/ for the top 100 songs of a specific date to be provided by the user. It uses the external libraries Requests, Spotipy, BeautifulSoup and Flask, as well as Bootstrap's CDN for basic styling.
