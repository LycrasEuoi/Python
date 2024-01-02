import os
import requests
import urllib.parse

from datetime import datetime
from flask import Flask, jsonify, redirect, request, session
from dotenv import load_dotenv

# Initialize Flask application
app = Flask(__name__)
app.secret_key = "Gk8wHkq02fFuZoXY7Go6NSbzpjPkMEzxHFZnJn1N6"

# Load environment variables
load_dotenv()

# Spotify API configuration
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"
PLAYLIST = os.getenv("PLAYLIST")

@app.route("/")
def login():
    """Redirect to Spotify authentication screen."""
    scope = ("""user-read-private
             user-read-email
             user-read-currently-playing
             playlist-modify-public
             playlist-modify-private
             playlist-read-private""")
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "show_dialog": True
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)

@app.route("/callback")
def callback():
    """Handle Spotify authentication callback."""
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
        update_session_tokens(token_info)
        return redirect("/hub")


@app.route("/refresh-token") # checking for refresh code and sending it.
def refresh_token():
    """Refresh the Spotify access token."""
    if "refresh_token" not in session:
        return redirect("/")
    if datetime.now().timestamp() > session["expires_at"]:
        req_body = {
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET
        }
        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()
        update_session_tokens(new_token_info)
        return redirect("/hub")
    
@app.route("/hub")
def create_hub_page():
    """Create the hub page."""
    validate_token()
    return ("""<h1><center><a style="text-decoration:none" href='/playlists'>Get users playlist</a><br>
            <a style="text-decoration:none" href='/current_song'>Get users current playing song</a><br>
            <a style="text-decoration:none" href='/add_current_song'>Add current song to playlist</a><br>
            <a style="text-decoration:none" href='/add_to_playlist'>Add song to playlist with check</a>""")


@app.route("/current_song")
def get_current_song():
    """Get the current song playing on the user's Spotify."""
    validate_token()
    response = simpel_api_call("me/player/currently-playing?market=NL")
    song_info=format_song_info(response)
    return song_info

@app.route("/playlists")
def get_playlist():
    """Retrieve the user's playlists."""
    playlists = simpel_api_call("me/playlists")
    return playlists

@app.route("/add_current_song")
def add_current_song_to_playlist():
    """Add the current playing song to the user's playlists."""
    validate_token()
    response =  simpel_api_call("me/player/currently-playing?market=NL")
    session["song_id"] = response["item"]["id"]
    headers = {
        "Authorization": f"Bearer {session["access_token"]}",
        "Content-Type": "application/json"
    }
    data = {
    "uris": [f"spotify:track:{session['song_id']}"] 
    }
    requests.post(f"{API_BASE_URL}playlists/{PLAYLIST}/tracks", headers=headers, json=data)
    return redirect("/hub") 

@app.route("/add_to_playlist")
def test():
    headers = {"Authorization": f"Bearer {session["access_token"]}"}
    current_playlist = requests.get(f"{API_BASE_URL}playlists/{PLAYLIST}/tracks?market=NL&fields=items(track(name))", headers=headers).json()
    current_song_playing = simpel_api_call("me/player/currently-playing?market=NL")
    list_of_songs = [item["track"]["name"] for item in current_playlist["items"]]
    if current_song_playing["item"]["name"] in list_of_songs:
        return "already in playlist"
    return redirect("/add_current_song")

def validate_token():
    """Validate if the access token is retrieved and valid"""
    if "access_token" not in session:
        return redirect("/")
    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")
    
def simpel_api_call(endpoint):
    """Simpel API Call function"""
    headers = {"Authorization": f"Bearer {session["access_token"]}"}
    response = requests.get(API_BASE_URL + endpoint, headers=headers)
    resp_json = response.json()
    return resp_json

def update_session_tokens(token_info):
    """Updates the token if it's expired"""
    session["access_token"] = token_info['access_token']
    session["refresh_token"] = token_info.get('refresh_token', session["refresh_token"])
    session["expires_at"] = datetime.now().timestamp() + token_info['expires_in']

def format_song_info(response):
    """Format song information into a readable string."""
    if 'item' in response and response['item']:
        song_id = response["item"]["id"]
        song_name = response["item"]["name"]
        artists = response["item"]["artists"]
        artists_names = ', '.join([artist["name"] for artist in artists])
        return f"{song_id} - {song_name} - {artists_names}"
    else:
        return "No song is currently playing."
    
#def is_current_song_in_playlist():

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)