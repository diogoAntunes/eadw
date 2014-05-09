import imdb
import sys
sys.path.append('./RecomendationSystems')
from soupTools import *

# Returns the userID movies and there rating
def getUserMovies(userID):
	
	userMovies = dict()
	userMovies = userMongoGetUser(userID)

	return userMovies

# Insert the movie in the db
# Search IMDb for the movie URL
# Fetch the information from Beautiful Soup

def movieNotFound(movie):

	print "MOVIE NOT FOUND: ", movie
	movieNoRate = linecache.getline('u.item', movie)
	movieParsed = movieNoRate.split("|")
	movieName = movieParsed[1]
	imdbMovieURL = imdbGetMovieURL(movieName)
	rating, des = getRatings(imdbMovieURL)
	imdbMongoAddMovie(movie, des, rating)

	return rating


# Returns the IMDb URL for the movieName
# used for Beautiful Soup parsing
def imdbGetMovieURL(movieName):
	ia = imdb.IMDb()
	searchResult = ia.search_movie(movieName)[0]
	url = ia.get_imdbURL(searchResult)
	
	return url


# Search the IMDb for the rating
# of the movie with the movieName
# if no rate was found, the average
# of the rates is returned (3)
def moviesRating(movieName):

	ia = imdb.IMDb()
	searchResult = ia.search_movie(movieName)[0]
	imdbID = searchResult.movieID
	
	try:
		s_result = ia.get_movie(imdbID)	
		keys = s_result.keys()

		if 'rating' in keys:
			return s_result['rating']
	except:
		print 'No Rate'
		return 3



def getUserMoviesRating(userMovies):

	#  mudar tudo para nova mongoDB
	userMoviesRating = dict()
	imdbRate = 0
	userRate = 0

	# userMovies = {'movieID' : 'rating'}
	# buscar o rating dos users movies ao imdb
	# imdbMongoGetMovie(movieID)
	for movie in userMovies.keys():
		rating = imdbMongoGetMovieRating(movie)

		# if the movie was not found in the db
		# fetch for the new movie and insert it
		if rating == 'no movie':
			rating = movieNotFound(movie)

		# if the movie was found in the db
		# but couldnt retrieve the rating
		# set the rate to the average rating
		if rating is None:
			rating = 6

		# If rate is 0
		# fetch the rate on IMDb
		# IMDb needs the movie Title to fetch movie
		# information, retrieve the title from the Setting File
		if float(rating) == 0:
			movieNoRate = linecache.getline('./Settings/u.item', movie)
			movieParsed = movieNoRate.split("|")
			movieName = movieParsed[1]
			rating = moviesRating(movieName)
			imdbMongoSetRate(movie, rating)
		

		# Total Sum of the imdb ratings
		# and the user ratings
		userRate += float(userMovies[movie])
		imdbRate += float(rating)/2
		userMoviesRating[movie] = {
			"rating" : userMovies[movie],
			"imdb" : float(rating)/2
		}

	userMoviesRating['userRate'] = userRate
	userMoviesRating['imdbRate'] = imdbRate

	return userMoviesRating



def getIMDbRS(predictedMovieID, userID):
	
	userMovies = getUserMovies(userID)
	userMoviesRating = getUserMoviesRating(userMovies)

	sizeUserMovies = len(userMovies)

	# Average of the IMDb Rates
	# and the User Rates
	uRate = (userMoviesRating['userRate'])/(sizeUserMovies)
	imdbRate = (userMoviesRating['imdbRate'])/(sizeUserMovies)
	
	# Difference between the averages
	pred = imdbRate - uRate	

	# Get the IMDb Rating of the predicted movie
	predMovieRate = imdbMongoGetMovieRating(predictedMovieID)

	# If no movie was found in the db
	# fetch the rate using Beautiful Soup
	if predMovieRate == 'no movie':
		predMovieRate = movieNotFound(predictedMovieID)
				
	# calculate the prediction of the rate
	predReturn = ((float(predMovieRate)/2) - (pred))

	if int(predReturn) == 0:
		return 1
	else:
		return int(predReturn)