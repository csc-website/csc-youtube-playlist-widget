import json
import os
from datetime import datetime

import requests

API_KEY = os.environ["YOUTUBE_API_KEY"]
PLAYLIST_ID = "PLa-g29pgu3Osw8pLpADbygS0OyNopp6Qc"
LIMIT = 5

API_URL = "https://www.googleapis.com/youtube/v3/playlistItems"

params = {
    "part": "snippet,contentDetails",
    "playlistId": PLAYLIST_ID,
    "maxResults": 50,
    "key": API_KEY,
}

response = requests.get(API_URL, params=params, timeout=30)
response.raise_for_status()

data = response.json()

if "error" in data:
    raise RuntimeError(data["error"])

videos = []

for item in data.get("items", []):
    snippet = item.get("snippet", {})
    resource = snippet.get("resourceId", {})

    video_id = resource.get("videoId")
    title = snippet.get("title", "").strip()
    published = snippet.get("publishedAt")

    if not video_id or not title or not published:
        continue

    thumbnails = snippet.get("thumbnails", {})

    thumbnail = (
        thumbnails.get("medium", {}).get("url")
        or thumbnails.get("high", {}).get("url")
        or thumbnails.get("default", {}).get("url")
    )

    if not thumbnail:
        thumbnail = f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg"

    dt = datetime.fromisoformat(published.replace("Z", "+00:00"))

    videos.append(
        {
            "title": title,
            "date": dt.strftime("%m/%d/%Y"),
            "link": f"https://www.youtube.com/watch?v={video_id}",
            "thumbnail": thumbnail,
            "published": published,
        }
    )

videos = videos[:LIMIT]

if len(videos) < LIMIT:
    raise RuntimeError(
        f"Found only {len(videos)} usable videos. Expected at least {LIMIT}."
    )

for video in videos:
    video.pop("published", None)

with open("videos.json", "w", encoding="utf-8") as file:
    json.dump(videos, file, indent=2, ensure_ascii=False)

print(f"Updated videos.json with {len(videos)} videos.")
