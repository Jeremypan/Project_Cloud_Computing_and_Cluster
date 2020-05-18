import re
from textblob import TextBlob
import couchdb
import nltk
nltk.download('punkt')

server = couchdb.Server("http://admin:password@172.26.130.78:5984/")
read_dbname='harvester'
upadte_dbname='covid_sentiment'
read_db=server[read_dbname]
if upadte_dbname in server:
        upadte_db = server[upadte_dbname]
else:
    upadte_db = server.create(upadte_dbname)

#process_amount=read_db.info()['doc_count']
process_amount=100
mango={'selector':{},'fields':['_id','full_text',"place"],'limit':process_amount}
result=read_db.find(mango)

#Remove http link, # and @ in the text in order to get tweet sentiment
http = re.compile('[http|https]*://[a-zA-Z0-9.?/&_%=:]*', re.S)
hashtag_at=re.compile('[@|#][a-zA-Z0-9.?/&_=%:]*', re.S)

covid_strings=['covid','virus']

#Is the tweet related to covid
for i in result:
    if i['full_text'].lower().find('covid')>=0:
        covid_related=True
    elif i['full_text'].lower().find('virus')>=0:
        covid_related=True
    else:
        covid_related=False
    #Get sentiment
    tweet_text = re.sub(hashtag_at,'',re.sub(http, '', i['full_text']))
    tweet_tb=TextBlob(tweet_text)
    
    upadte_db.save({'_id':i['_id'],'covid_related':covid_related,'sentiment':tweet_tb.sentiment[1],'place':i["place"]})
    
    
    
    