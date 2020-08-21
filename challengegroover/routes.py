from flask import Blueprint, redirect, request, jsonify, render_template
import os
from .spotify_auth import SpotifyAuth
from .spotify_req import SpotifyReq
from tinydb import TinyDB, Query
from datetime import date

# Landing page of the app.
root = Blueprint("root", "root", url_prefix="/")
db = TinyDB("db.json")
releases = db.table("releases")


@root.route("/")
def index():
    return render_template("index.html")


# Spotify Authorization.
auth = Blueprint("auth", "auth", url_prefix="/auth")


@auth.route("/")
def get_user():
    response = SpotifyAuth().getUser()
    return redirect(response)


@auth.route("/callback")
def callback():
    code = request.values["code"]
    tokens = SpotifyAuth().getUserToken(code)
    os.environ['ACCESS_TOKEN'] = tokens["access_token"]
    #updating database once a day only
    if db.storage.read() == None or (db.search(Query().lastUpdate == str(date.today()))) == []:
        SpotifyReq().getNewReleases(os.environ['ACCESS_TOKEN'])
    return jsonify(tokens)


# API
api = Blueprint("api", "api", url_prefix="/api")

# Add your "artists" route here.
@api.route("/artists")
def get_artists():
    return jsonify(releases.all())