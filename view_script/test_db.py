import couchdb
from couchdb import design

remote_sever = couchdb.Server('http://admin:password@172.26.133.161:5984/')
for db in remote_sever:
    print(db)
harvester_db = remote_sever['harvester']


# docs=[doc for doc in harvester_db]
# sample_doc=docs[:10]
# print(sample_doc)
# ['1000009822824091650', '1000032464356683776', '1000303211196989441', '1000406370640973824', '1000474464851640320', '1000609415513260032', '1000653917166845952', '1000909741604810752', '1000915677237071873', '1000916744658075648']
# ['_id', '_rev', 'created_at', 'id', 'id_str', 'full_text', 'truncated', 'display_text_range', 'entities', 'source', 'in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name', 'user', 'geo', 'coordinates', 'place', 'contributors', 'is_quote_status', 'retweet_count', 'favorite_count', 'favorited', 'retweeted', 'possibly_sensitive', 'lang']
# for doc_id in sample_doc:
#     print(harvester_db[doc_id]['full_text'])
def view_unprocessed_raw(db):
    """Create a view of all unprocessed tweets in raw tweets db."""
    map_fnc = """
    function (doc) {
        var text=doc.full_text.toLowerCase();
        var flag=false;
        var str=["covid","coronouvars"];
        for (var i =0; i<str.length;i++){
            if (text.indexOf(str[i])>= 0){
                flag=true;
                break;
              }
        }
    if (flag){
    emit([doc._id,doc.user.id_str,doc.full_text], [doc.place.name,doc.place.bounding_box.coordinates]);
    }
}
    """
    red_fnc = """function (keys,values,rereduce){
        return count(values);
}
    """
    view = design.ViewDefinition(
        'raw_text', 'covid_text_statistic', map_fnc, red_fnc
    )
    view.sync(db)


view_unprocessed_raw(harvester_db)
