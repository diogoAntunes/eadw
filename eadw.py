import sys
sys.path.append('./Tools')
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

	


# print imdbPrediction(264, 3)
# Movie prediction
# User 3:
# Todos os filmes que ele deu rate
# guardar rateUser -- rateIMDB
# se o rate for 0 e necessario ir ao imdb
# actualizar na database
# calcular o desvio
# user pede movie X
# ir ao imdb ver o movie X e adicionar o desvio

def textSimIndex():

	schema = Schema(itemID = NUMERIC(stored=True), content=TEXT, rating = NUMERIC(stored=True))

	if not os.path.exists("indexdir"):
	  os.mkdir("indexdir")

	#This creates a storage object to contain the index    
	ix = create_in("indexdir", schema)

	#Add documents to index
	writer = ix.writer()

	#PESQUISA NO MONGODB
	docs = imdbMongoGetAllMovies()

	for doc in docs:
		itemID = doc['id']
		content = doc['des']
		rating = doc['rating']
		writer.add_document(itemID= itemID, content= content, rating= float(rating))

	writer.commit()

# textSimIndex()

# Recomendar ao user
# procurar o movie mais rated do user
# retirar a descricao, pesquisar no whoosh por movies
# semelhantes e retirar os 3 mais

def findSim(userID):

	# Movie mais rated do user
	userMovies = userMongoGetUser(userID)
	print userMovies
	max(userMovies.iteritems(), key=operator.itemgetter(1))[0]
 

	ix = open_dir("indexdir")

	with ix.searcher() as searcher:
		query = QueryParser("userID",ix.schema,group=OrGroup).parse(b)
		results = searcher.search(query,limit=10000)
		for r in results:
			ratesB[r['itemID']] = r['rating']

def user(userID):
	# Movie mais rated do user
	userMovies = userMongoGetUser(userID)
	print userMovies
	
	maxRateMovie = max(userMovies.iteritems(), key=operator.itemgetter(1))[0]

	movieIMDB = imdbMongoGetMovie(maxRateMovie)

	des = movieIMDB['des']
	print des

	ix = open_dir("indexdir")

	with ix.searcher() as searcher:
		query = QueryParser("content",ix.schema,group=OrGroup).parse(des)
		results = searcher.search(query,limit=100)
		for r in results:
			print r.score
			print r['itemID']

def recomendMovie(userID):

	userMovies = userMongoGetUser(userID)
	maxRateMovie = max(userMovies.iteritems(), key=operator.itemgetter(1))[0]
	print maxRateMovie
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
		
	return recomend['itemID']


# recomendMovie(3)

# user(3)
# 320 - 688

# user saca o movie com mais cotation e a des
# imdb 10 movies mais pros
# indexar no whoosh
# calcular a similiraty
# sugerir 2