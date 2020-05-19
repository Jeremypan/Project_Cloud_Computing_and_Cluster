import json
import couchdb
from dblogin import user, password
import sys

server = couchdb.Server("http://%s:%s@localhost:5984/" % (user, password))
dbname = "aurin"
if dbname in server:
    db = server[dbname]
else:
    db = server.create(dbname)

def read_datajson(file_path):
    with open(file_path, 'r') as f:
        line = f.read()
        # print(line)
        temp = json.loads(line)
        data = temp.get('features')
        count = 0
        for each_data in data:
            new_data = data[count]
            count = count + 1
            db.save(new_data)



read_datajson("data346406433645962701.json")
read_datajson("data476356061098611510.json")
read_datajson("data816774669468958420.json")
read_datajson("data991522153697550829.json")
read_datajson("data1349714280269167671.json")
read_datajson("data1522858704156841645.json")
read_datajson("data2620750029319500392.json")
read_datajson("data3837786783944013920.json")
read_datajson("data3870122785782773619.json")
read_datajson("data4617994025021873553.json")
read_datajson("data4618836278611028213.json")
read_datajson("data4710699998445470851.json")
read_datajson("data4777088166829996656.json")
read_datajson("data5170475016279481688.json")
read_datajson("data5440978485986338504.json")
read_datajson("data6461467032473569942.json")
read_datajson("data7094146846941056959.json")
read_datajson("data7134773239019724824.json")
read_datajson("data7155575918718235924.json")
read_datajson("data7576789349692613083.json")
read_datajson("data8008749898353742663.json")
read_datajson("data8225712414233867008.json")
read_datajson("data9011032496127305714.json")
