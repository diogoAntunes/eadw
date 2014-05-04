
# class MoviesTools:

# Get the genre of every user movie
def getGenre(movieID, userMovies):
	
	moviesGenre = dict()
	# unknown | Action | Adventure | Animation |
	# Childrens | Comedy | Crime | Documentary | 
	# Drama | Fantasy | Film-Noir | Horror | 
	# Musical | Mystery | Romance | Sci-Fi |Thriller | 
	# War | Western |
	f = open("u.item", "r")

	for movie in f:
			movieParsed = movie.split("|")
			movieID = int(movieParsed[0])
			if movieID in userMovies.keys():
					genres = movieParsed[5:]
					moviesGenre[movieID] = []
					for genre in genres:
							moviesGenre[movieID].append(int(genre))
	return moviesGenre

def getRatings(id, userMovies):

	f = open("u.item", "r")
	
	moviesGenre = getGenre(id, userMovies)
	movieFound = dict()
	relevance = dict()

	for movie in f:
			movieParsed = movie.split("|")
			movieID = int(movieParsed[0])
			if movieID == id:
					genres = movieParsed[5:]
					movieFound[movieID] = []
					for genre in genres:
							movieFound[movieID].append(int(genre))
	
	
	if len(movieFound.keys()) != 0:
			a = []
			for k, v in enumerate(movieFound[id]):
					if v == 1:
							a.append(k)
			lenA = len(a)
			for movie in moviesGenre:
					b = []
					for k, v in enumerate(moviesGenre[movie]):
							if v == 1:
									b.append(k)
					intersect = len(set(a).intersection(set(b)))
					if lenA >=3:
							if intersect >= (len(a)-1):
									relevance[movie] = intersect
					else:
							if intersect >= lenA:
									relevance[movie] = intersect
	return relevance

def getMovieRating(movieID, userMovies):

	rates = getRatings(movieID, userMovies)
	somRate = 0
	somIntersect = 0
	for rate in rates:
		somRate += userMovies[rate] * rates[rate]
		somIntersect += rates[rate]

	total = float(somRate)/somIntersect
	print "MovieID: ", movieID
	print "RatingPrediction: ", total
	print "RealRating: ", userMovies[movieID]

	# av = 0
	# for rate in rates:
	# 	av += userMovies[rate]

	# 	print float(av)/len(rates)