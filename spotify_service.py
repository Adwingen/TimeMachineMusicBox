# spotify_service.py
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from cover import create_cover_image
import os

CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")

if not CLIENT_ID or not CLIENT_SECRET or not REDIRECT_URI:
    raise RuntimeError("Variáveis de ambiente Spotify não configuradas")



def get_spotify_oauth():
    return SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope="playlist-modify-private ugc-image-upload",
        cache_path="token.txt",
        show_dialog = True,  # <- força re-consentimento
    )


def create_playlist(sp, date: str, songs: list[str], progress):
    artist_image_url = None
    artist_name = None

    progress["status"] = "search"
    progress["message"] = "A procurar músicas no Spotify..."
    progress["total"] = len(songs)
    progress["current"] = 0

    user_id = sp.current_user()["id"]
    year = date.split("-")[0]
    song_uris = []

    for idx, song in enumerate(songs, start=1):
        result = sp.search(q=f"track:{song} year:{year}", type="track", limit=1)
        items = result["tracks"]["items"]

        if items:
            track = items[0]
            song_uris.append(track["uri"])

            if not artist_image_url:
                artist = track["artists"][0]
                artist_name = artist["name"]

                artist_data = sp.artist(artist["id"])
                images = artist_data["images"]

                if images:
                    artist_image_url = images[0]["url"]

        progress["current"] = idx

    progress["status"] = "adding"
    progress["message"] = "A adicionar músicas à playlist..."

    playlist = sp.user_playlist_create(
        user=user_id,
        name=f"{date} Billboard 100",
        public=False,
        description=f"Top 100 da Billboard em {date}"
    )

    sp.playlist_add_items(playlist["id"], song_uris)

    progress["status"] = "cover"
    progress["message"] = "A criar capa personalizada..."

    try:
        if artist_image_url:
            cover_base64 = create_cover_image(
                date,
                artist_name,
                artist_image_url
            )
            sp.playlist_upload_cover_image(
                playlist["id"],
                cover_base64
            )
    except Exception:
        progress["status"] = "warning"
        progress["message"] = "Playlist criada, mas sem capa personalizada."

    progress["status"] = "done"
    progress["message"] = "Playlist criada com sucesso 🎉"
    progress["playlist_url"] = playlist["external_urls"]["spotify"]

    return playlist["external_urls"]["spotify"]





