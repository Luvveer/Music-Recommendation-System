import spotipy  
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv
import os

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIFY_CLIENT_SECRET =os.getenv('SPOTIFY_CLIENT_SECRET')

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id= SPOTIFY_CLIENT_ID,
    client_secret=SPOTIFY_CLIENT_SECRET
))

MOOD_TO_GENRE = {
    "happy":"happy hits",
    "sad":"sad songs",
    "angry":"chill",
    "neutral":"rock",
    "excited":"party hits",
}

def get_songs_for_mood(mood):
    query = MOOD_TO_GENRE.get(mood,"chill") + "track"
    results = sp.search(q = query, limit = 20, type = "track")

    #print("Spotify Search Results:", results)
    songs = []
    for track in results["tracks"]["items"]:
        song = {
            "name": track["name"],
            "artist": track["artists"][0]["name"],
            "url": track["external_urls"]["spotify"],
            "image": track["album"]["images"][0]["url"]
        }
        songs.append(song)

    #    print(f"Song Name: {song['name']}")
    #    print(f"Artist: {song['artist']}")
    #    print(f"URL: {song['url']}\n")
    #    print(f"Image URL: {song['image']}\n")
    return songs