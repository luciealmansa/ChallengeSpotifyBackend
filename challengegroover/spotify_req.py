import base64, json, requests, os
import sys;
from flask import jsonify
from tinydb import TinyDB, Query
from datetime import date, datetime
import json


class SpotifyReq(object):
    HEADER = "application/x-www-form-urlencoded"
    SPOTIFY_URL_RELEASES = "https://api.spotify.com/v1/browse/new-releases"
    RELEASE_LIMIT = 50
    RELEASE_OFFSET = 0
    ARTIST_ID_LIMIT = 50
    db = TinyDB("db.json")
    releases = db.table("releases")


    def getNewReleases(self, access_token):
        
        self.releases.truncate()

        headers = {
            "Content-Type": self.HEADER,
            "Authorization": f"Bearer {access_token}",
        }

        self.db.upsert({"lastUpdate" : str(date.today())}, Query().lastUpdate.exists())

        #while we can still get releases from the API
        while True:
            body = {
            "limit": self.RELEASE_LIMIT,
            "offset": self.RELEASE_OFFSET
            }
            getReleases = requests.get(self.SPOTIFY_URL_RELEASES, params=body, headers=headers).json()
            for release in getReleases["albums"]["items"]:
                for i in range(len(release["artists"])):
                    self.releases.insert({
                        "artist" : release["artists"][i]["name"],
                        "album" : release["name"],
                        "releaseDate" : self.formatDate(release["release_date"]),
                        "coverURL" : release["images"][0]["url"]
                    })
            self.RELEASE_OFFSET = self.RELEASE_OFFSET + self.RELEASE_LIMIT

            if getReleases["albums"]["next"] == None:
                break

        return

    
    def formatDate(self, dateString):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        dateFormat = datetime.strptime(dateString, '%Y-%m-%d')
        return months[dateFormat.month - 1] + ", " + str(dateFormat.day)
