import json
from datetime import datetime

HISTORY_FILE = "history.json"


def save_playlist(date, playlist_url):
    with open(HISTORY_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    data.append({
        "date": date,
        "url": playlist_url,
        "created_at": datetime.now().isoformat()
    })

    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
