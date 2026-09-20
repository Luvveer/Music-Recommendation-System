# Music Recommendation System

A Flask web app that reads a short piece of text describing how you feel, classifies the mood with TextBlob sentiment analysis, and recommends a set of tracks pulled live from the Spotify Web API, complete with album art and Spotify links.

![Music Recommendation System screenshot](static/screenshot.png)
*(Screenshot placeholder — replace `static/screenshot.png` with an actual screenshot or short GIF of the app in use.)*

## Features

- Detects mood from free-text input using TextBlob sentiment analysis (happy, sad, angry, excited, neutral).
- Maps each mood to a Spotify search query/genre and fetches matching tracks via [spotipy](https://spotipy.readthedocs.io/).
- Displays song name, artist, album cover, and a direct Spotify link.
- Simple, responsive UI with Spotify-themed styling and hover animations.

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

Everything runs server-side per request — there is no database, background job, or caching layer beyond the Spotify auth token cache spotipy writes to disk (see Security below).

## Prerequisites

- Python 3.9+
- A Spotify account (free or premium) to create a developer application
- pip for installing dependencies

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
2. Click **Create app**, give it a name/description, and accept the terms.
3. Once created, open the app and copy the **Client ID** and **Client Secret** (click "View client secret").
4. This app only calls the Client Credentials Flow (no user login), so no redirect URI needs to be configured for it to work, though the dashboard requires one to be set — any placeholder URL (e.g. `http://localhost:8888/callback`) satisfies that requirement.

## Environment variables

Create a `.env` file in the project root (this file is gitignored and must never be committed):

```
SPOTIFY_CLIENT_ID=your_spotify_client_id
SPOTIFY_CLIENT_SECRET=your_spotify_client_secret
```

`Utils/spotify.py` loads these via `python-dotenv` at import time.

## Running the app

```bash
python Server.py
```

Then open `http://127.0.0.1:5000/` in your browser. The app runs in Flask debug mode by default (see `Server.py`) — turn this off before any real deployment.

## Limitations of the sentiment analysis

The mood detection is intentionally simple and has real limitations:

- **TextBlob's polarity score is lexicon-based**, not context-aware — it doesn't understand negation nuance, sarcasm, idioms, or mixed emotions well (e.g. "I'm not sad" or "great, another Monday" can be misclassified).
- Only **polarity** is used, not subjectivity, so factual/neutral-sounding statements about strong emotions may be classified as "neutral."
- The five mood buckets are derived from **arbitrary fixed thresholds** (`> 0.5`, `< -0.5`, `< 0`, `> 0`) rather than a trained classifier, so borderline scores can flip category with small wording changes.
- TextBlob has no awareness of emojis, slang, or multi-language input; results are least reliable outside of plain, literal English text.
- Because mood maps to a fixed, small set of Spotify search queries (`MOOD_TO_GENRE` in `Utils/spotify.py`), recommendations are coarse-grained rather than personalized.

This is fine for a demo/hobby project but should not be treated as accurate emotional inference.

## Security note

Spotify credentials (`SPOTIFY_CLIENT_ID`, `SPOTIFY_CLIENT_SECRET`) must **only** live in your local `.env` file, which is excluded from version control via `.gitignore`. Never commit `.env`, hardcode credentials in source files, or paste them into issues/commits.

Note also that spotipy writes a `.cache` file to disk containing OAuth tokens after authenticating — this is also gitignored and should never be committed. If credentials or cached tokens are ever accidentally committed, rotate them immediately from the Spotify Developer Dashboard, since git history retains old commits even after a file is later removed.

## Future improvements

- Add speech-to-text input for moods.
- Personalized playlists based on listening history.
- Integrate YouTube Music / Apple Music as alternate sources.
- Replace lexicon-based sentiment analysis with a trained mood classifier.

## Suggested repository description and topics

**Description:** Flask + Spotify web app that recommends music based on the mood detected in your text, using TextBlob sentiment analysis.

**Topics:** `flask` `python` `spotify` `spotify-api` `spotipy` `textblob` `sentiment-analysis` `nlp` `music-recommendation` `mood-detection`
