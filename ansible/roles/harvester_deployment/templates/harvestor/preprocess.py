import couchdb
import json
from dblogin import user, password
import re
import nltk
from textblob import TextBlob

def covidsentiment(doc):
    keywords = ["covid","coronavirus"]
    http = re.compile('[http|https]*://[a-zA-Z0-9.?/&_%=:]*', re.S)
    hashtag_at = re.compile('[@|#][a-zA-Z0-9.?/&_=%:]*', re.S)
    try :
        text = doc["full_text"].lower()
        if (any (x in text for x in keywords)):
            doc["covid"] = True
        else:
            doc["covid"] = False

        tweet_text = re.sub(hashtag_at,'',re.sub(http, '', doc["full_text"]))
        tweet_tb = TextBlob(tweet_text)
        doc["sentiment"] = tweet_tb.sentiment[0]
        return doc
    except :
        return None

if __name__ == "__main__":
    nltk.download('punkt')
    server = couchdb.Server("http://%s:%s@:5984/" % (user,password))
    db = server["harvester"]

    for row in db.view("_all_docs"):
        key = row["key"]
        doc = covidsentiment(db[key])
        if doc is None:
            print("This is not a proper document")
        else:
            db[key] = doc

    print("Finished preprocessing database")


    
