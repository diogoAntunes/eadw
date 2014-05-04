from whoosh.index import open_dir
from whoosh.qparser import  *
import re

# class UserTools:



def getUserMovies(userID):
	userMovies = dict()
	ix = open_dir("indexdir")
	
	with ix.searcher() as searcher:
	    query = QueryParser("userID",ix.schema,group=OrGroup).parse(str(userID))
	    results = searcher.search(query,limit=100)
	    for r in results:
	        userMovies[r['itemID']] = r['rating'] 
	
	print userMovies       
	return userMovies