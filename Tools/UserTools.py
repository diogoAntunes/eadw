from whoosh.index import open_dir
from whoosh.qparser import  *
#from imdbTools import *
#from mongoDBTools import *
import re
import linecache


def getUserMovies(userID):
	userMovies = dict()
	userMovies = userMongoGetUser(userID)
	
# Returns the rating of the movies
# the user has rated

def getUserMoviesRating(userMovies, predictID):

	#  mudar tudo para nova mongoDB
	userMoviesRating = dict()
	imdbRate = 0
	userRate = 0

	# userMovies = {'movieID' : 'rating'}
	# buscar o rating dos users movies ao imdb
	# imdbMongoGetMovie(movieID)
	for movie in userMovies.keys():
		rating = imdbMongoGetMovie(movie)['rating']
		# If rate is 0
		# fetch imdbpy or rt
		# imdb needs the movie tittle
		if float(rating) == 0:
			movieNoRate = linecache.getline('u.item', movie)
			movieParsed = movieNoRate.split("|")
			movieName = movieParsed[1]
			rating = moviesRating(movieName)
			imdbMongoSetRate(movie, rating)
		
		userRate += float(userMovies[movie])
		imdbRate += float(rating)/2
		userMoviesRating[movie] = {
			"rating" : userMovies[movie],
			"imdb" : float(rating)/2
		}

# 	userMoviesRating['userRate'] = userRate
# 	userMoviesRating['imdbRate'] = imdbRate

# 	return userMoviesRating
