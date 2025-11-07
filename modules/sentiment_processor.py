# modules/sentiment_processor.py
import random

def analyze_sentiment(text, method="naive_bayes"):
    # simulasi hasil dummy (sementara)
    sentiments = ["positive", "neutral", "negative"]
    sentiment = random.choice(sentiments)
    confidence = round(random.uniform(0.7, 0.99), 2)
    return {
        "method": method,
        "sentiment": sentiment,
        "confidence": confidence,
    }
