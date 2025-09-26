from textblob import TextBlob 

def detect_mood(text):
    sentiment = TextBlob(text).sentiment
    polarity = sentiment.polarity

    print("Sentiment polarity", polarity)
    if polarity > 0.5:
        return "happy"
    elif polarity < -0.5:
        return "sad"
    elif polarity < 0:
        return "angry"
    elif polarity > 0:
        return "excited"
    else:
        return "neutral"