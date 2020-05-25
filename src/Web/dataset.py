import couchdb


def tolist(view):
    alist = []
    for i in view:
        alist.append({'city': i.key, 'value': i.value})
    return alist


def combine(list1, list2):
    result = []
    for i in list1:
        for j in list2:
            if (i['city'] == j['city']):
                result.append([i['value'], j['value'], i['city']])
    result = sorted(result, key=lambda i: i[0])
    return result;


# choose server
server = couchdb.Server('http://admin:admin@172.26.129.213:5984')

# choose db
dbname1 = "harvester"
dbname2 = "aurin"
if dbname1 in server and dbname2 in server:
    harvester = server[dbname1]
    aurin = server[dbname2]
else:
    harvester = server.create(dbname1)
    aurin = server.create(dbname2)

view_income = aurin.view('analysis/mean_income_by_city')
view_covid = harvester.view('analysis/covid_by_city', group_level=1)
view_sentiment = harvester.view('analysis/sentiment_by_city', group_level=1)
view_population = aurin.view('analysis/population_by_city')

target = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Newcastle', 'Canberra',
          'Sunshine Coast', 'Geelong', 'Hobart', 'Central Coast']

pop_by_region = []
income_by_region = []
tot_income = []
income_list = []
pop_list = []
covid_list = []
sentiment_list = tolist(view_sentiment)

for i in view_population:
    for j in view_income:
        if i.key == j.key and i.key != 'Hunter Valley exc Newcastle':
            pop_by_region.append({'city': i.key, 'value': i.value})
            income_by_region.append({'city': i.key, 'value': i.value * j.value})

for i in target:
    tot = 0
    for j in pop_by_region:
        if i in j['city']:
            tot += j['value']
    pop_list.append({'city': i, 'value': tot})

i = 0
while i < len(target):
    tot = 0
    for j in income_by_region:
        if target[i] in j['city']:
            tot += j['value']
    income_list.append({'city': target[i], 'value': round(tot / pop_list[i]['value'])})
    i += 1

for i in view_covid:
    for j in pop_list:
        if i.key == j['city']:
            covid_list.append({'city': j['city'], 'value': i.value / j['value']})
