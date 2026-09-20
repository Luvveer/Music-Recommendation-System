# Music Recommendation System

A Flask app that reads a sentence about how you're feeling, runs it through TextBlob for sentiment, and pulls back a set of matching tracks from Spotify with album art and links.

## Features

- Detects mood from free-text input (happy, sad, angry, excited, neutral)
- Maps each mood to a Spotify search query and fetches matching tracks via [spotipy](https://spotipy.readthedocs.io/)
- Shows song name, artist, album cover, and a Spotify link for each result
- Simple, responsive UI with Spotify-themed styling

## Architecture and request flow

```
Browser (templates/index.html)
      │  POST /  { mood: "<free text>" }
      ▼
Server.py (Flask route "/")
      │
      ├─► Utils/sentiment.py: detect_mood(text)
      │       TextBlob(text).sentiment.polarity → one of
      │       happy / sad / angry / excited / neutral
      │
      └─► Utils/spotify.py: get_songs_for_mood(mood)
              MOOD_TO_GENRE[mood] → Spotify search query
              spotipy.Spotify(...).search(...) → track list
              (name, artist, album image, Spotify URL)
      ▼
Server.py renders templates/index.html with the song list
      ▼
Browser displays recommended tracks
```

Everything happens server-side, per request. There's no database or background job. The only thing written to disk is the Spotify auth token cache that spotipy manages (see Security below).

## Prerequisites

- Python 3.9+
- A Spotify account, to register a developer application
- pip

## Installation

```bash
git clone https://github.com/<your-username>/Music-Recommendation-System.git
cd Music-Recommendation-System
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Spotify developer application setup

1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in.
2. Click "Create app", fill in a name and description, and accept the terms.
3. Open the new app and copy the Client ID and Client Secret ("View client secret").
4. This app only uses the Client Credentials flow, so it never asks a user to log in. The dashboard still requires a redirect URI to be set even though nothing will hit it, so any placeholder like `http://localhost:8888/callback` works.

## Environment variables

Create a `.env` file in the project root (gitignored, never commit it):

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

`Utils/spotify.py` loads these with `python-dotenv` on import.

## Running the app

```bash
python Server.py
```

Open `http://127.0.0.1:5000/`. The app runs in Flask debug mode by default (`Server.py`); turn that off before deploying anywhere real.

## Limitations of the sentiment analysis

The mood detection is a small lexicon lookup, not a real emotion model, and it shows:

- TextBlob's polarity score doesn't handle negation, sarcasm, idioms, or mixed emotions well. "I'm not sad" or "great, another Monday" can come out wrong.
- Only polarity is used, not subjectivity, so a flatly-stated strong emotion can land as "neutral."
- The five mood buckets come from fixed thresholds (`> 0.5`, `< -0.5`, `< 0`, `> 0`), not a trained classifier, so a slight rewording can flip the result across a boundary.
- No handling for emojis, slang, or non-English text. It works best on plain, literal English.
- `MOOD_TO_GENRE` in `Utils/spotify.py` maps each mood to one fixed search query, so results are generic rather than personalized.

Good enough for a demo. Don't read too much into what it says about your actual mood.

## Security

Keep `SPOTIFY_CLIENT_ID` and `SPOTIFY_CLIENT_SECRET` in your local `.env` file only. Don't hardcode them, commit `.env`, or paste them into an issue or commit message.

spotipy also writes a `.cache` file with your OAuth token after the first run. That's gitignored too. If a credential or cache file ever does get committed, rotate it from the Spotify dashboard right away, since removing the file later doesn't remove it from git history.

## Future improvements

- Speech-to-text input for moods
- Personalized playlists based on listening history
- YouTube Music / Apple Music as alternate sources
- A trained mood classifier instead of TextBlob's lexicon scoring

## Suggested repository description and topics

Description: Flask + Spotify app that recommends music based on the mood in your text, using TextBlob sentiment analysis.

Topics: `flask` `python` `spotify` `spotify-api` `spotipy` `textblob` `sentiment-analysis` `nlp` `music-recommendation` `mood-detection`
