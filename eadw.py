import sys
sys.path.append('../Tools')
from UserTools import *
from MoviesTools import *
from pprint import pprint
from mongoDBTools import *
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os
import re
import operator
import linecache

# Devia de se ter os sistemas de prediction todos divididos
# e depois chamava-se aqui um a um com o seu devido peso
def getPrediction(movieID, userID):
	userMovies = getUserMovies(userID)
	bla = getMovieRating(movieID, userMovies)
	return bla
# getPrediction(264, 3)

def imdbPrediction(movieID, userID):
	
	userMovies = getUserMovies(userID)
	userMoviesRating = getUserMoviesRating(userMovies, movieID)

	sizeUserMovies = len(userMovies)

	uRate = (userMoviesRating['userRate'])/(sizeUserMovies)
	imdbRate = (userMoviesRating['imdbRate'])/(sizeUserMovies)
	
	pred = imdbRate - uRate	

	# pprint(userMoviesRating)

	# print "prediction", pred
	predMovieRate = imdbMongoGetMovieRating(movieID)

	if predMovieRate == 'no movie':
		predMovieRate = movieNotFound(movieID)
				
	predReturn = ((float(predMovieRate)/2) - (pred))

	if int(predReturn) == 0:
		return 1
	else:
		return int(predReturn)		


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
		rating = imdbPrediction(recomend['itemID'], userID)
		
		iID2 = recomend2['itemID']
		title2 = movieParsed2[1]
		rating2 = imdbPrediction(recomend2['itemID'], userID)

		return iID, rating, title, iID2, rating2, title2


# print recomendMovie(3)

# user(3)
# 320 - 688

# user saca o movie com mais cotation e a des
# imdb 10 movies mais pros
# indexar no whoosh
# calcular a similiraty
# sugerir 2