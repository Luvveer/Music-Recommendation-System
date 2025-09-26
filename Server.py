from flask import Flask, request, jsonify, render_template 
from Utils.sentiment import detect_mood
from Utils.spotify import get_songs_for_mood

app = Flask(__name__) 

@app.route("/", methods =["Get","POST"])
def index():
    recommended_songs = []
    if request.method == "POST":
        mood_text = request.form.get("mood", "")
        if mood_text:
            mood = detect_mood(mood_text)
            recommended_songs = get_songs_for_mood(mood)
    return render_template("index.html",songs = recommended_songs) 


if __name__=="__main__":
    app.run(debug=True) 

