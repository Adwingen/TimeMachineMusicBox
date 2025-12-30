import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint


def get_spotify_uris(sp, songs: list[str], year: str) -> list[str]:
    song_uris = []

    for song in songs:
        query = f"track:{song} year:{year}"

        try:
            result = sp.search(q=query, type="track", limit=1)
            items = result["tracks"]["items"]

            if not items:
                print(f"❌ Não encontrada no Spotify: {song}")
                continue

            uri = items[0]["uri"]
            song_uris.append(uri)
            print(f"✅ Encontrada: {song}")

        except Exception as e:
            print(f"⚠️ Erro ao procurar '{song}': {e}")

    return song_uris

def create_playlist_and_add_songs(sp, user_id: str, date: str, song_uris: list[str]):
    playlist_name = f"{date} Billboard 100"

    playlist = sp.user_playlist_create(
        user=user_id,
        name=playlist_name,
        public=False,
        description=f"Top 100 músicas da Billboard em {date}"
    )

    playlist_id = playlist["id"]

    sp.playlist_add_items(
        playlist_id=playlist_id,
        items=song_uris
    )

    print(f"\n🎉 Playlist criada com sucesso!")
    print(f"📀 Nome: {playlist_name}")
    print(f"🎶 Músicas adicionadas: {len(song_uris)}")


def scrape_hot_100_titles(date: str) -> list[str]:
    url = f"https://www.billboard.com/charts/hot-100/{date}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    title_tags = soup.select("li h3#title-of-a-story")

    titles = [tag.get_text(strip=True) for tag in title_tags if tag.get_text(strip=True)]
    titles = titles[:100]

    return titles


def main():
    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=CLIENT_ID,
            client_secret=CLIENT_SECRET,
            redirect_uri=REDIRECT_URI,
            scope="playlist-modify-private",
            cache_path="token.txt"
        )
    )

    user = sp.current_user()
    user_id = user["id"]
    print(f"Autenticado como: {user_id}")

    date = input("Para que data quer viajar? (YYYY-MM-DD): ")
    year = date.split("-")[0]

    songs = scrape_hot_100_titles(date)
    song_uris = get_spotify_uris(sp, songs, year)

    create_playlist_and_add_songs(sp, user_id, date, song_uris)




if __name__ == "__main__":
    main()

