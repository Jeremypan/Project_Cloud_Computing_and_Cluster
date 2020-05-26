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
    return result


# choose server
server = couchdb.Server('http://admin:admin@localhost:5984')

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
    if i.value is None:
        continue
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

inter = combine(sentiment_list, covid_list)
map_col = [['Lat', 'Long', 'Avg Sentiment Score', 'Number of tweets about covid per 10000 person']]

target = ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Newcastle', 'Canberra',
          'Sunshine Coast', 'Geelong', 'Hobart', 'Central Coast']
coord = {'Sydney': [-33.8688, 151.2093], 'Melbourne': [-37.8136, 144.9631], 'Brisbane': [-27.4698, 153.0251],
         'Perth': [-31.9505, 115.8605], 'Adelaide': [-34.9285, 138.6007], 'Gold Coast': [-28.0167, 153.4000],
         'Newcastle': [-32.9283, 151.7817], 'Canberra': [-35.2809, 149.1300], 'Sunshine Coast': [-26.6500, 153.0667],
         'Geelong': [-38.1499, 144.3617], 'Hobart': [42.8821, 147.3272], 'Central Coast': [-33.3208, 151.2336]}
for i in inter:
    map_col.append([coord[i[2]][0], coord[i[2]][1], i[0], i[1]*10000])
