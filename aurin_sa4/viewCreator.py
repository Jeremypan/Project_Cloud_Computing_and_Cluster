import couchdb
import json
from dblogin import user, password
import sys

server = couchdb.Server("http://%s:%s@localhost:5984/" % (user, password))
db = server["aurin"]
with open("/home/ubuntu/CCC/aurin_sa4/view_aurin.json") as file_object:
    db["_design/analysis"] = json.load(file_object)