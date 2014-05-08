from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
import re

#This schema has two fields: id and content
schema = Schema(userID = NUMERIC(stored=True), itemID = NUMERIC(stored=True), rating = NUMERIC(stored=True))

if not os.path.exists("indexdir"):
    os.mkdir("indexdir")

#This creates a storage object to contain the index    
ix = create_in("indexdir",schema)

#Add documents to index
writer = ix.writer()

#Document interation
#Open file
file = open("u1.base")

# 196	242	3	881250949
# user id | item id | rating | timestamp
for line in file:
	doc = re.split('\W+', line)	
	userID = int(doc[0])
	itemID = int(doc[1])
	rating = int(doc[2])
	writer.add_document(userID=userID, itemID=itemID, rating=rating)

writer.commit()