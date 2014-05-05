from whoosh.index import open_dir
from whoosh.qparser import  *
from imdbTools import *
from mongoDBTools import *
import re

def getUserMovies(userID):
	userMovies = dict()
	ix = open_dir("indexdir")
	
	with ix.searcher() as searcher:
	    query = QueryParser("userID",ix.schema,group=OrGroup).parse(str(userID))
	    results = searcher.search(query,limit=100)
	    for r in results:
	        userMovies[r['itemID']] = r['rating'] 
	
	# print userMovies   
	return userMovies

# Returns the rating of the movies
# the user has rated
def getUserMoviesRating(userMovies):

	userMoviesRating = dict()
	imdbRate = 0
	userRate = 0

	f = open("./Util/u.item", "r")

	for movie in f:
		movieParsed = movie.split("|")
		movieID = int(movieParsed[0])
		if movieID in userMovies.keys():
			movieName = movieParsed[1].encode('utf-8')
			rating = mongoFindMovie(movieName)
			# If rate is 0
			# fetch imdbpy or rt
			if float(rating) == 0:
				rating = moviesRating(movieName)
			
			userRate += float(userMovies[movieID])
			imdbRate += float(rating)
			userMoviesRating[movieID] = {
				"title" : movieName,
				"rating" : userMovies[movieID],
				"imdb" : rating
			}

	userMoviesRating['userRate'] = userRate
	userMoviesRating['imdbRate'] = imdbRate

	return userMoviesRating