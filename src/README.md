Current Verison:
 - it needs to stop harverster to avoid re-indexing of the view thanks to the big batch upd

Suggested improvement:
 - reset view option to stale view with update seq (then keep runnning harvester and return stale view to client if the new re-indexing has not been done.
 - ref: https://docs.couchdb.org/en/stable/api/ddoc/views.html?highlight=View#view-options
 
 
