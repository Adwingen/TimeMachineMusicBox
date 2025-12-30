# app.py
import spotipy
import json

from billboard import scrape_hot_100_titles
from spotify_service import create_playlist, get_spotify_oauth
from flask import Flask, render_template, request, redirect, session
from flask import jsonify
import threading
from history import save_playlist



progress_state = {
    "status": "idle",
    "message": "",
    "current": 0,
    "total": 0,
    "playlist_url": ""
}




app = Flask(__name__)
app.secret_key = "dev-secret-key"  # qualquer string para dev

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        date = request.form["date"]

        # 👉 guardar na sessão
        session["date"] = date

        auth_url = get_spotify_oauth().get_authorize_url()
        return redirect(auth_url)

    return render_template("index.html")

@app.route("/callback")
def callback():
    oauth = get_spotify_oauth()
    code = request.args.get("code")
    oauth.get_access_token(code)

    sp = spotipy.Spotify(auth_manager=oauth)

    date = session.get("date")
    songs = scrape_hot_100_titles(date)

    progress_state.update({
        "status": "search",
        "message": "A procurar músicas...",
        "current": 0,
        "total": len(songs),
        "playlist_url": ""
    })

    def background_task():
        try:
            playlist_url = create_playlist(sp, date, songs, progress_state)

            progress_state["playlist_url"] = playlist_url

            # ✅ guardar no histórico
            save_playlist(date, playlist_url)

        except Exception as e:
            progress_state["status"] = "error"
            progress_state["message"] = str(e)

    threading.Thread(target=background_task, daemon=True).start()

    # 🔑 ISTO É O QUE ESTAVA A FALTAR
    return render_template("progress.html")



@app.route("/progress")
def progress():
    return jsonify(progress_state)

@app.route("/history")
def history():
    with open("history.json", encoding="utf-8") as f:
        data = json.load(f)

    # ordenar do mais recente para o mais antigo
    data = list(reversed(data))

    return render_template("history.html", history=data)






if __name__ == "__main__":
    app.run(debug=True)
