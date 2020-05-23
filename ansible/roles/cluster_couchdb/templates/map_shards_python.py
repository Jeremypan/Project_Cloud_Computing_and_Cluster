"""script for map out cluster to exsited database -- retrieve volumes data"""

import requests
import json
url_admin='http://{}:{}@{}:{}/_membership'.format("admin", "admin","localhost","5984")
url_shards= 'http://{}:{}@{}:{}/_node/_local/_dbs/harvester'.format("admin", "admin","localhost","5984")
response_shards=requests.get(url_shards)
response_admin= requests.get(url_admin)
shards=json.loads(response_shards.content)
admins=json.loads(response_admin.content)
new_node_list=admins['all_nodes']
current_node=admins['all_nodes']
format=shards.copy()
document=[]
old_nodes=[]
for i in format['changelog']:
    document.append(i[1])
    if i[2] not in new_node_list:
        i[0]="remove"
    old_nodes.append(i[2])
old_nodes=list(set(old_nodes))
for i in old_nodes.copy():
    if i in new_node_list:
        old_nodes.remove(i)

document=list(set(document))
for node in new_node_list:
    if node in old_nodes:
        continue
    else:
        for doc in document:
            format['changelog'].append(["add",doc,node])
print(old_nodes)
by_node=format['by_node'].copy()
for k,v in by_node.items():
    if k in new_node_list:
        continue
    else:
        del format['by_node'][k]
for node in new_node_list:
    if node not in by_node.keys():
        format['by_node'][node]=document

by_range=format['by_range'].copy()
for k,v in by_range.items():
    for ref_node in v:
        if v in new_node_list:
            continue
        else:
            v.remove(ref_node)
        for new_node in new_node_list:
            if new_node not in v:
                v.append(new_node)
url_put_harvester='http://{}:{}@{}:{}/_node/_local/_dbs/harvester'.format("admin", "admin","localhost","5984")
url_put_users='http://{}:{}@{}:{}/_node/_local/_dbs/_users'.format("admin", "admin","localhost","5984")
url_put_replicator='http://{}:{}@{}:{}/_node/_local/_dbs/_replicator'.format("admin", "admin","localhost","5984")
url_put_global_changes='http://{}:{}@{}:{}/_node/_local/_dbs/_global_changes'.format("admin", "admin","localhost","5984")
url_put_aurin='http://{}:{}@{}:{}/_node/_local/_dbs/aurin'.format("admin", "admin","localhost","5984")
url_database_sync='http://{}:{}@{}:{}/harvester/_sync_shards'.format("admin", "admin","localhost","5984")
result=json.loads(requests.put(url_put_harvester,json=format).content)


def run_loads(format,url):
    temp=json.loads(requests.get(url).content)
    format['_rev']=temp['_rev']
    format['_id']=temp['_id']
    return json.loads(requests.put(url,json=format).content)

print(run_loads(format,url_put_users))
print(run_loads(format,url_put_replicator))
print(run_loads(format,url_put_global_changes))
print(run_loads(format,url_put_aurin))
print(requests.post(url_database_sync).content)


