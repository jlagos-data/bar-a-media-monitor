import requests
import json
import pandas as pd
import os
from dotenv import load_dotenv
from textblob import TextBlob
from sqlalchemy import create_engine
from datetime import datetime, timedelta

load_dotenv()
API_KEY = os.getenv("NEWS_API_KEY")

def extract_news(query="FC BARCELONA"):
    url = f"https://newsapi.org/v2/everything"
    now = datetime.now()
    from_date = (now - timedelta(days=3)).strftime("%Y-%m-%dT%H:%M:%SZ")
    to_date = now.strftime("%Y-%m-%dT%H:%M:%SZ")
    params = {
        "q": query,
        "from": from_date,
        "to": to_date,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY
        
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        articles = data.get("articles", [])

        results = [
            {
                "title": art["title"],
                "description": art["description"],
                "url": art["url"],
                "publishedAt": art["publishedAt"],
                "source": art["source"]["name"],
            }
            for art in articles
        ]
        return results
    else:
        print(f"Error al obtener noticias: {response.status_code}")
        return []


def process_news(news_list):
    if not news_list:
        print("No se encontraron noticias")
        return pd.DataFrame()

    df = pd.DataFrame(news_list)
    df["publishedAt"] = pd.to_datetime(df["publishedAt"])
    df["title"] = df["title"].fillna("")
    df["description"] = df["description"].fillna("")
    df["full_text"] = df["title"] + " " + df["description"]
    df = df.sort_values("publishedAt", ascending=False)
    return df

def analyze_sentiment(df):
    if df.empty:
        return df
    
    def sentymel_label(text):
        analysis = TextBlob(text)
        popularity = analysis.sentiment.polarity

        if popularity > 0:
            return "positive"
        elif popularity < 0:
            return "negative"
        else:
            return "neutral"

    df["sentiment"] = df["full_text"].apply(sentymel_label)
    return df
    
def save_to_db(df, db_name="reputation.db"):
    if df.empty:
        return
    
    engine = create_engine(f"sqlite:///{db_name}")
    df.to_sql("news", con=engine, if_exists="replace", index=False)
    print(f"{len(df)} noticias guardados exitosamente en {db_name}")
    

raw_data = extract_news()
processed_data = process_news(raw_data)
analyzed_data = analyze_sentiment(processed_data)
save_to_db(analyzed_data)
