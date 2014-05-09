from whoosh.index import open_dir
from whoosh.qparser import  *
from imdbTools import *
from mongoDBTools import *
from soupTools import *
import re
import linecache


def getUserMovies(userID):
	userMovies = dict()
	userMovies = userMongoGetUser(userID)
	
# Returns the rating of the movies
# the user has rated
	return userMovies

def getUserMoviesRating(userMovies, predictID):

	#  mudar tudo para nova mongoDB
	userMoviesRating = dict()
	imdbRate = 0
	userRate = 0

	# userMovies = {'movieID' : 'rating'}
	# buscar o rating dos users movies ao imdb
	# imdbMongoGetMovie(movieID)
	for movie in userMovies.keys():
		rating = imdbMongoGetMovieRating(movie)

		if rating == 'no movie':
			rating = movieNotFound(movie)

		if rating is None:
			rating = 6

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

	userMoviesRating['userRate'] = userRate
	userMoviesRating['imdbRate'] = imdbRate

	return userMoviesRating

def movieNotFound(movie):

	print "BAD MOVIE"
	movieNoRate = linecache.getline('u.item', movie)
	movieParsed = movieNoRate.split("|")
	movieName = movieParsed[1]
	imdbMovieURL = imdbGetMovieURL(movieName)
	rating, des = getRatings(imdbMovieURL)
	imdbMongoAddMovie(movie, des, rating)

	return rating
