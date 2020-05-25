import couchdb
from dblogin import user, password
import json

# choose server
server = couchdb.Server('http://%s:%s@localhost:5984' % (user,password))
print(server.version())

# choose db
dbname = "harvester"
if dbname in server:
    db = server[dbname]
else:
    db = server.create(dbname)
for dbname in server:
    print(dbname)

# create view
if ("_design/analysis" in db): 
    print("The views already exist")
else:
    with open("/home/ubuntu/harvestor/harvesterview.json") as file_object:
        db["_design/analysis"] = json.load(file_object)
print("Finished creating views")
