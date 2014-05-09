import sys
sys.path.append('./DataBaseTools')
from mongoDBTools import *

# Get the genre of every userMovie
def getGenre(userMovies):
	
	moviesGenre = dict()
	# Genre List:
	# 
	# unknown | Action | Adventure | Animation |
	# Childrens | Comedy | Crime | Documentary | 
	# Drama | Fantasy | Film-Noir | Horror | 
	# Musical | Mystery | Romance | Sci-Fi |Thriller | 
	# War | Western |
	f = open("./Settings/u.item", "r")

	# for every movie in the userMovies
	# retrieve the gender of that movie
	# form the file "u.item"
	for movie in f:
		movieParsed = movie.split("|")
		movieID = int(movieParsed[0])
		if movieID in userMovies.keys():
			genres = movieParsed[5:]
			moviesGenre[movieID] = []
			for genre in genres:
				moviesGenre[movieID].append(int(genre))
					
	return moviesGenre


# Returns the relevance of every movie
# { movieID : relevance }
def getRatings(predictMovieID, userMovies):

	f = open("./Settings/u.item", "r")
	
	# Gets the genre of every user movie
	moviesGenre = getGenre(userMovies)
	movieFound = dict()
	relevance = dict()

	# for each movie in the "u.item"
	# search for the predictedMovieID and save the gender
	for movie in f:
		movieParsed = movie.split("|")
		movieID = int(movieParsed[0])
		if movieID == predictMovieID:
			genres = movieParsed[5:]
			movieFound[movieID] = []
			for genre in genres:
				movieFound[movieID].append(int(genre))

	# If no error occured and the predictedMovieID
	# was found and the gender retrived
	if len(movieFound.keys()) != 0:
		a = []

		# Save the genders that are selected for the predictedMovieID
		# a[] contains the position of array where the gender is 1
		for k, v in enumerate(movieFound[predictMovieID]):
			if v == 1:
				a.append(k)
		
		lenA = len(a)

		# for every movie in the userMovies
		# Save the genders that are selected
		# b[] contains the position of array where the gender is 1
		for movie in moviesGenre:
			b = []
			for k, v in enumerate(moviesGenre[movie]):
				if v == 1:
					b.append(k)
			
			# Get the intersection betwen the genders in the predictedMovieID
			# and the movie in userMovies
			intersect = len(set(a).intersection(set(b)))

			# Improvements to the rating system:
			# if the predicted movie has more then 3 genders
			# and at least the same amount or more genders 
			# then the userMovie, we rate is relevance equal to the intersection
			# between both
			if lenA >=3:
				if intersect >= (len(a)-1):
					relevance[movie] = intersect
			else:
				if intersect >= lenA:
					relevance[movie] = intersect
	
	return relevance


# Returns the userID movies and there rating
def getUserMovies(userID):
	
	userMovies = dict()
	userMovies = userMongoGetUser(userID)

	return userMovies


# Returns a prediction for the movie with the
# predictedMovieID
def getMovieRatingPrediction(predictedMovieID, userMovies):

	rates = getRatings(predictedMovieID, userMovies)

	total = 3
	somRate = 0
	somIntersect = 0
	for rate in rates:
		somRate += userMovies[rate] * rates[rate]
		somIntersect += rates[rate]

	if (somIntersect != 0):
		total = float(somRate)/somIntersect
	#print "MovieID: ", movieID
	#print "RatingPrediction: ", total
	#print "RealRating: ", userMovies[movieID]
	
	return total


def getGenderRS(predictedMovieID, userID):
	
	userMovies = getUserMovies(userID)
	prediction = getMovieRatingPrediction(predictedMovieID, userMovies)
	
	if int(prediction) == 0:
		return 1
	else:
		return int(prediction)