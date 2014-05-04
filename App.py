from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
from UserTools import *
from MoviesTools import *
import os
import re
 
def getPrediction(movieID, userID):

	# movies = MoviesTools()
	# users = UserTools()

	userMovies = getUserMovies(userID)
	# print userMovies
	getMovieRating(movieID, userMovies)


