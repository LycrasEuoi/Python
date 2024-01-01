import requests
import os
import urllib.parse

from dotenv import load_dotenv
from datetime import datetime
from flask import *

app = Flask(__name__)
app.secret_key = "Gk8wHkq02fFuZoXY7Go6NSbzpjPkMEzxHFZnJn1N6"

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"

AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"

PLAYLIST = os.getenv("PLAYLIST")


@app.route("/") # opening screen to spotify OAuth app
def index():
    return "Welcome to my Spotify App <br><a href='/login'>Login with Spotify</a>"


@app.route("/login") # redirecting to auth screen of spotify
def login():
    scope = "user-read-private user-read-email user-read-currently-playing playlist-modify-public playlist-modify-private"

    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "show_dialog": True
    }

    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)


@app.route("/callback") # callback for error's
def callback():
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})
    
    if "code" in request.args:
        req_body = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()


        session["access_token"] = token_info['access_token']
        session["refresh_token"] = token_info['refresh_token']
        session["expires_at"] = datetime.now().timestamp() +   token_info['expires_in']

        return redirect("/hub")


@app.route("/refresh-token") # checking for refresh code and sending it.
def refresh_token():

    if "refresh_token" not in session:
        return redirect("/login")
    
    if datetime.now().timestamp() > session["expires_at"]:
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        session["access_token"] = new_token_info["access_token"]
        session["expires_at"] = datetime.now().timestamp() +   new_token_info['expires_in']

        return redirect("/hub")
    

@app.route("/hub")
def create_hub_page():
    return "<a href='/playlists'>Get users playlist</a><br><a href='/current_song'>Get users current playing song</a><br><a href='/get_playlist_id'>Add current song to playlist</a>"


@app.route("/current_song")
def get_current_song():
    if "access_token" not in session:
        return redirect("/login")
    
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")
    
    headers = {
        "Authorization": f"Bearer {session["access_token"]}"
    }

    response = requests.get(API_BASE_URL + "me/player/currently-playing?market=NL" , headers=headers)

    song_title = json.loads(response.content)["item"]["id"]

    return song_title

@app.route("/playlists")
def get_playlist():
    if "access_token" not in session:
        return redirect("/login")
    
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")
    
    headers = {
        "Authorization": f"Bearer {session["access_token"]}"
    }

    response = requests.get(API_BASE_URL + "me/playlists", headers=headers)
    playlists = response.json()

    return jsonify(playlists)

@app.route("/get_playlist_id")
def get_playlist_id():

    if "access_token" not in session:
        return redirect("/login")
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")
    
    headers = {
        "Authorization": f"Bearer {session["access_token"]}"
    }

    response = requests.get(API_BASE_URL + "me/player/currently-playing?market=NL" , headers=headers)
    session["song_id"] = json.loads(response.content)["item"]["id"]

    return redirect("/add_id_to_playlist")

@app.route("/add_id_to_playlist")
def add_id_to_playlist():

    headers = {
        "Authorization": f"Bearer {session["access_token"]}",
        "Content-Type": "application/json"
    }

    data = {
    "uris": [f"spotify:track:{session['song_id']}"] 
    }
    
    response = requests.post(f"{API_BASE_URL}playlists/{PLAYLIST}/tracks", headers=headers, json=data)

    # Error handling (example)
    if response.status_code == 201:
        print("Track added successfully.")
    else:
        print(f"Failed to add track: {response.status_code} {response.text}")

    return redirect("/hub") 
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)