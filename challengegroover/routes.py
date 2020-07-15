from flask import Blueprint, redirect, session, request, jsonify, render_template
from .spotify_auth import SpotifyAuth

auth = Blueprint("auth", "auth", url_prefix="/auth")


@auth.route("/")
def get_user():
    response = SpotifyAuth().getUser()
    return redirect(response)


@auth.route("/callback")
def callback():
    code = request.values["code"]
    tokens = SpotifyAuth().getUserToken(code)
    return jsonify(tokens)


root = Blueprint("root", "root", url_prefix="/")


@root.route("/")
def index():
    return render_template("index.html")
