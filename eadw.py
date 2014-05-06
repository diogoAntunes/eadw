import sys
sys.path.append('Tools')
from UserTools import *
from MoviesTools import *
from pprint import pprint

# Devia de se ter os sistemas de prediction todos divididos
# e depois chamava-se aqui um a um com o seu devido peso
def getPrediction(movieID, userID):
	userMovies = getUserMovies(userID)
	getMovieRating(movieID, userMovies)

# getPrediction(264, 3)

def imdbPrediction(movieID, userID):
	userMovies = getUserMovies(userID)
	userMoviesRating = getUserMoviesRating(userMovies)

	sizeUserMovies = len(userMovies)

	uRate = (userMoviesRating['userRate'])/(sizeUserMovies)
	imdbRate = (userMoviesRating['imdbRate'])/(sizeUserMovies)
	
	pred = imdbRate - uRate	

	pprint(userMoviesRating)

	print "prediction", pred
	# print len(userMoviesRating)


imdbPrediction(264, 3)
# Movie prediction
# User 3:
# Todos os filmes que ele deu rate
# guardar rateUser -- rateIMDB
# se o rate for 0 e necessario ir ao imdb
# actualizar na database
# calcular o desvio
# user pede movie X
# ir ao imdb ver o movie X e adicionar o desvio