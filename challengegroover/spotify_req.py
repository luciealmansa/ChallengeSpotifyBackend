import base64, json, requests, os
import sys;
from flask import jsonify
from tinydb import TinyDB, Query
from datetime import date, datetime


class SpotifyReq(object):
    HEADER = "application/x-www-form-urlencoded"
    SPOTIFY_URL_RELEASES = "https://api.spotify.com/v1/browse/new-releases"
    SPOTIFY_URL_ARTISTS = "https://api.spotify.com/v1/artists"
    RELEASE_LIMIT = 50
    RELEASE_OFFSET = 0
    ARTIST_ID_LIMIT = 50
    db = TinyDB("db.json")
    releases = db.table("releases")
    artists = db.table("artists")


    def getNewReleases(self, access_token):
        
        self.releases.truncate()

        headers = {
            "Content-Type": self.HEADER,
            "Authorization": f"Bearer {access_token}",
        }

        self.db.upsert({"lastUpdate" : str(date.today())}, Query().lastUpdate.exists())

        while "we can still get releases":
            body = {
            "limit": self.RELEASE_LIMIT,
            "offset": self.RELEASE_OFFSET
            }
            getReleases = requests.get(self.SPOTIFY_URL_RELEASES, params=body, headers=headers).json()
            self.releases.insert_multiple(getReleases["albums"]["items"])
            self.RELEASE_OFFSET = self.RELEASE_OFFSET + self.RELEASE_LIMIT

            if getReleases["albums"]["next"] == None:
                break

        return self.getArtists(access_token)
    
    def getArtists(self, access_token):
        self.artists.truncate()

        idList = self.getArtistsIdsFromDB()
        headers = {
            "Content-Type": self.HEADER,
            "Authorization": f"Bearer {access_token}",
        }
        body = {
            "ids" : idList
        }

        Release_album = Query()
        Artist = Query()

        for idString in idList :
            getArtists = requests.get(self.SPOTIFY_URL_ARTISTS + "?ids=" + idString, headers=headers).json()
            for item in getArtists["artists"] :
                album = self.releases.get(Release_album.artists.any(Artist.name == item["name"]))
                self.artists.insert(
                    {
                        "name" : item["name"],
                        "followers" : item["followers"]["total"],
                        "img_url" : item["images"][0]["url"],
                        "genres" : item["genres"] if item["genres"] != [] else [""],
                        "album_release" : album["name"],
                        "release_date" : self.formatDate(album["release_date"])
                    })
        return


    def getArtistsIdsFromDB(self):
        idList = []
        idListString = ""
        artist_count = 0
        for item in self.releases :
            for artist in item["artists"]:
                artist_count = artist_count + 1

                if (artist_count + 1) % self.ARTIST_ID_LIMIT == 0:
                    idListString = idListString + (artist["id"])
                    idList.append(idListString)
                    idListString = ""
                else:
                    idListString = idListString + (artist["id"]) + ","

        return idList
    
    def formatDate(self, dateString):
        months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        dateFormat = datetime.strptime(dateString, '%Y-%m-%d')
        return months[dateFormat.month - 1] + ", " + str(dateFormat.day)
