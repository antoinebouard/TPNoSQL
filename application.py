# Requires pymongo 3.6.0+
from bson.son import SON
from pymongo import MongoClient


from flask import Flask, g, redirect, render_template, request, session, url_for

client = MongoClient("mongodb://localhost:27017/")
database = client["audiotpnosql"]
collection = database["albums"]

app = Flask(__name__)

app.secret_key = b"\x98\xca\x17\xbfg/v\x1dB\x93Lu\xcf3\x93\xfa"

# Created with Studio 3T, the IDE for MongoDB - https://studio3t.com/

pipeline = [
    {
        u"$project": {
            u"_id": 0,
            u"albums": u"$$ROOT"
        }
    }, 
    {
        u"$lookup": {
            u"localField": u"albums.alb_art",
            u"from": u"artistes",
            u"foreignField": u"art_id",
            u"as": u"artistes"
        }
    }, 
    {
        u"$unwind": {
            u"path": u"$artistes",
            u"preserveNullAndEmptyArrays": False
        }
    }, 
    {
        u"$sort": SON([ (u"albums.alb_prix", 1), (u"albums.alb_nom", 1) ])
    }, 
    {
        u"$project": {
            u"albums.alb_nom": u"$albums.alb_nom",
            u"artistes.art_nom": u"$artistes.art_nom",
            u"albums.alb_prix": u"$albums.alb_prix",
            u"albums.alb_img": u"$albums.alb_img",
            u"_id": 0
        }
    }
]

cursor = collection.aggregate(
    pipeline, 
    allowDiskUse = True
)
try:
    albums = []
    for doc in cursor:
        albums.append(doc)
        print(doc)
finally:
    client.close()


@app.route("/", methods=["GET"])
def index():
   """ Show the bibliotheque """
   return render_template("bibliotheque.html", bibliotheque=albums)

# @app.route("/", methods=["GET"])
# def index():
#     """ Show the bibliotheque """
#     return render_template("bibliotheque.html", bibliotheque=doc)