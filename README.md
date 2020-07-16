# Groover Backend Challenge

Your goal is to create an app using the [spotify wep api](https://developer.spotify.com/documentation/web-api/).
We have already provided you with a flask project able to authenticate to spotify.
Your job is to add two new features:
 - A way to fetch data from spotify's new releases API and persist it somewhere. for example using [TinyDB](https://tinydb.readthedocs.io/en/stable/intro.html)
 - A route : `/api/artists/` returning a JSON containing informations about artists that have released new tracks recently.

# How to run this sample

- move to this directory
- setup a new virtualenv and activate it
- install the requirements in requirements.txt
- run:
```
FLASK_ENV=development \
  CLIENT_ID=<the client id we gave you> \
  CLIENT_SECRET=<the client secret we gave you> \
  flask run
```
- go to http://localhost:5000/
- You can now log to spotify through the app.

# Project Structure

The initialisation of the app is done in **./challengegroover/__init__.py**.
The spotify auth is located in **./challengegroover/spotify_auth.py**. The flow ends with a call to `/auth/callback/` which will give you the necessary access tokens.
New routes can be added in **./challengegroover/routes.py**
Feel free to move and re-organise as you please, we expect a well organised and clean code.
