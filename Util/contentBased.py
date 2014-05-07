from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
import re

schema = Schema(itemID = NUMERIC(stored=True), content=TEXT, rating = NUMERIC(stored=True))

if not os.path.exists("indexContent"):
    os.mkdir("indexContent")

#This creates a storage object to contain the index    
ix = create_in("indexContent",schema)

#Add documents to index
writer = ix.writer()

#PESQUISA NO MONGODB
writer.add_document(userID=userID, itemID=itemID, rating=rating)

writer.commit()