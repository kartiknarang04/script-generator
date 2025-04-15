import os
import re
import json
import string
import requests
import pandas as pd
from collections import Counter, defaultdict
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import spacy
from googleapiclient.discovery import build
import matplotlib.pyplot as plt
from wordcloud import WordCloud


from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os

API_KEY = "AIzaSyBA_yvKYS53OQ0UdO7rnu4pk5tHGZOf9kg"
# Just to be sure your credentials aren't being overridden
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

YOUTUBE = build("youtube", "v3", developerKey=API_KEY, static_discovery=False)

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Setup
API_KEY = os.getenv("YOUTUBE_API_KEY")  # Make sure to set this in your .env or environment variables

REGION_CODE = "IN"

# Extra YouTube-specific stopwords
EXTRA_STOPWORDS = {"subscribe", "channel", "watch", "video", "instagram", "facebook", "youtube", 
                   "official", "tv", "like", "share", "follow", "live", "new", "us", "join", "today"}
STOPWORDS = set(stopwords.words("english")).union(EXTRA_STOPWORDS)
ps = PorterStemmer()

# Functions
def clean_text(text):
    text = text.lower()
    text = re.sub(r"[\r\n]+", " ", text)
    text = text.translate(str.maketrans('', '', string.punctuation))
    return text

def extract_phrases(text):
    doc = nlp(text)
    return [chunk.text.lower() for chunk in doc.noun_chunks if chunk.text.lower() not in STOPWORDS]

def stem_keywords(keywords):
    stem_map = defaultdict(list)
    for word in keywords:
        root = ps.stem(word)
        stem_map[root].append(word)
    final_counts = {min(set(v), key=len): len(v) for k, v in stem_map.items() if len(v) > 1}
    return final_counts

def get_trending_videos(region_code=REGION_CODE, max_results=100):
    request = YOUTUBE.videos().list(
        part="snippet",
        chart="mostPopular",
        regionCode=region_code,
        maxResults=50  # YouTube allows only 50 per request
    )
    response = request.execute()
    videos = response.get("items", [])

    # If more needed
    while len(videos) < max_results and "nextPageToken" in response:
        request = YOUTUBE.videos().list(
            part="snippet",
            chart="mostPopular",
            regionCode=region_code,
            maxResults=50,
            pageToken=response["nextPageToken"]
        )
        response = request.execute()
        videos.extend(response.get("items", []))

    return videos[:max_results]

def analyze_videos(videos):
    category_keywords = defaultdict(list)
    
    for video in videos:
        snippet = video['snippet']
        title = clean_text(snippet.get("title", ""))
        description = clean_text(snippet.get("description", ""))
        tags = snippet.get("tags", [])
        category_id = snippet.get("categoryId", "unknown")

        full_text = f"{title} {description} " + (" ".join(tags) + " ") * 3

        phrases = extract_phrases(full_text)
        phrases = [word for word in phrases if word not in STOPWORDS]
        category_keywords[category_id].extend(phrases)

    category_analysis = {}
    for cat_id, words in category_keywords.items():
        counts = stem_keywords(words)
        top_words = sorted(counts.items(), key=lambda x: x[1], reverse=True)[:10]
        category_analysis[cat_id] = top_words

    return category_analysis

def visualize_trends(category_analysis):
    for cat_id, trends in category_analysis.items():
        words, freqs = zip(*trends)
        plt.figure(figsize=(10, 5))
        plt.bar(words, freqs)
        plt.title(f"Top Trends for Category ID {cat_id}")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        wc = WordCloud(width=800, height=400, background_color='white')
        wc.generate_from_frequencies(dict(trends))
        plt.figure(figsize=(10, 5))
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        plt.title(f"WordCloud for Category ID {cat_id}")
        plt.show()

# ---- MAIN ----
if __name__ == "__main__":
    print("Fetching trending videos...")
    trending_videos = get_trending_videos()

    print("Analyzing content...")
    analysis = analyze_videos(trending_videos)

    print(json.dumps(analysis, indent=2))

    print("Visualizing trends...")
    visualize_trends(analysis)
