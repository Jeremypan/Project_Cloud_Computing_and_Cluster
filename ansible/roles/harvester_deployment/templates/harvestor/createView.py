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
if ("_design/analysis" in db and "covid" in db["_design/analysis"]["views"] and "sentiment" in db["_design/analysis"]["views"]):
    print("The views already exist")
else:
    design_doc = {
        '_id': '_design/analysis', 
        'views': {
            'covid': {
                'map': 'function (doc) {if (doc.covid == true) {emit(doc.place.bounding_box, doc.covid);}}',
                'reduce':'_count'
            },
            'sentiment': {
                'map': 'function (doc) {emit(doc.place.bounding_box, doc.sentiment);}',
                'reduce': 'function (keys, values, rereduce) {return sum(values)/values.length;}'
            }
        },
        'language':'javascript'
    }
    db.save(design_doc)

print("Finished creating views")
