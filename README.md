# Music-Recommendation-System
This is a system that would input a text and interpret your mood and provide with the recommended songs appropriately.

This project is a Flask + Spotify-powered web application that recommends songs based on the user’s mood.
By analyzing text input with TextBlob (sentiment analysis), the app maps your emotional state (happy, sad, angry, neutral, excited) to curated Spotify playlists and displays recommended tracks with album covers and Spotify links.

Features:

    - Detects mood from the user input using TextBloc sentiment analysis.
    - Maps moods to specific Spotify playlists/genres.
    - Displays song details: name, artist, album cover, Spotify link.
    - Simple and clean UI with responsive design.
    - Hover animations and Spotify-themed styling.

Tech Stack:

    - Backend: Python,Flask
    - NLP: TextBlob
    - Music data: Spotify Web API (spotipy)
    - Frontend: HTML, CSS.

TO run the Code: python Server.py

Future improvements: 

    - Add speech-to-text input for moods.
    - Personalized playlists (based on listening history).
    - integrate YouTube Music/Apple Music options.
    
