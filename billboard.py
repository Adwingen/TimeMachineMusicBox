# billboard.py
import requests
from bs4 import BeautifulSoup


def scrape_hot_100_titles(date: str) -> list[str]:
    url = f"https://www.billboard.com/charts/hot-100/{date}"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    title_tags = soup.select("li h3#title-of-a-story")

    titles = [tag.get_text(strip=True) for tag in title_tags]
    return titles[:100]
