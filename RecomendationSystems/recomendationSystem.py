from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
import re
import operator
import linecache
import sys
from imdbRS import *
sys.path.append('./DataBaseTools')
from mongoDBTools import *

# Recomend a Movie to the user
def recomendMovie(userID):

	userMovies = userMongoGetUser(userID)
	maxRateMovie = max(userMovies.iteritems(), key=operator.itemgetter(1))[0]

	topMovies = imdbMongoGetTopMovies()

	movieIMDB = imdbMongoGetMovie(maxRateMovie)

	des = movieIMDB['des']

	schema = Schema(itemID = NUMERIC(stored=True), content=TEXT, rating = NUMERIC(stored=True))

	if not os.path.exists("indexdir"):
	  os.mkdir("indexdir")

	#This creates a storage object to contain the index    
	ix = create_in("indexdir", schema)

	#Add documents to index
	writer = ix.writer()

	for movie in topMovies:
		itemID = movie['itemID']
		content = movie['content']
		rating = movie['rating']
		writer.add_document(itemID= itemID, content= content, rating= float(rating))

	writer.commit()
	
	with ix.searcher() as searcher:
		query = QueryParser("content",ix.schema,group=OrGroup).parse(des)
		results = searcher.search(query,limit=100)
		
		recomend = results[0]
		movieNoRate = linecache.getline('u.item', recomend['itemID'])
		movieParsed = movieNoRate.split("|")

		recomend2 = results[1]
		movieNoRate2 = linecache.getline('u.item', recomend2['itemID'])
		movieParsed2 = movieNoRate2.split("|")
		
		iID = recomend['itemID']
		title = movieParsed[1]
		rating = getIMDbRS(recomend['itemID'], userID)
		
		iID2 = recomend2['itemID']
		title2 = movieParsed2[1]
		rating2 = getIMDbRS(recomend2['itemID'], userID)

		return iID, rating, title, iID2, rating2, title2
