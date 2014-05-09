from pymongo import MongoClient

def newMongoConnection():
	client = MongoClient('localhost', 27017)
	return client


# USER MONGO TOOLS

# Returns dict() with:
# { movieID : rating }
def userMongoGetUser(userID):
	client = newMongoConnection()
	db = client.test
	users = db.users

	doc = users.find_one({"userID": userID})
	client.disconnect()

	userToReturn = dict()
	
	movies = doc['movies']
	for movie in movies:
		userToReturn[movie['itemID']] = movie['rating']

	return userToReturn


# IMDB MONGO TOOLS

# Gets the IMDb rating of the movie
# with the movieID
# if no movie was found with such movieID
# 'no movie' is returned
def imdbMongoGetMovieRating(movieID):
	client = newMongoConnection()
	db = client.test
	imdb = db.imdb
	doc = imdb.find_one({'id' : movieID})
	client.disconnect()

	if doc:
		return doc['rating']
	else:
		return 'no movie'


# Add a new movie to the db
def imdbMongoAddMovie(movieID, des, rating):

	print 'ADDING MOVIE'
	print 'Movie ID: ', movieID
	print 'Movie Description: ', des
	print 'Movie Rating: ', rating

	client = newMongoConnection()
	db = client.test
	imdb = db.imdb
	newMovie = {'id' : movieID, 'rating' : rating, 'des' : des}
	imdb.insert(newMovie)

	client.disconnect()


# Updates the Rating of the movie with
# the movieID
def imdbMongoSetRate(movieID, newRating):
	
	print 'UPDATING RATING'
	print 'Movie ID: ', movieID
	print 'Movie Rating : ', newRating

	client = newMongoConnection()
	db = client.test
	imdb = db.imdb
	
	imdb.update({"id" : movieID}, {"$set": {"rating" : newRating}})
	client.disconnect()


def mongoFindItem(itemID, sameMovies, prediction):
	
	client = newMongoConnection()
	db = client.test
	users = db.users

	# users que tem o pred movie ou pelo menos
	# um movie igual ao user
	# docs = users.find({"itemID": itemID})
	
	docs = db.users.find({'movies.itemID' : {"$all" : [itemID, prediction]}})
	
	client.disconnect()

	# users que tem pelo menos um movie igual 
	# ao do user, e tem o predMovie
	for doc in docs:
		sameMovies.append(doc['userID'])

	return sameMovies


# Returns the average of the ratings
# of the user with the userID
def mongoGetAVG(userID):
	
	client = newMongoConnection()
	db = client.test
	imdb = db.users
	query = [{"$match": {"userID": userID}}, {"$unwind":"$movies"}, 
			{"$project": {"_id" : 0, "q" :"$query", "i" :"$movies.rating"}}, 
			{"$group" : {"_id": "$q", "av": {"$avg" : "$i"}}}]

	results = db.users.aggregate(query, cursor = {})

	for result in results:
		return result['av']



# Gets the top 10 movies from the db
def imdbMongoGetTopMovies():

	client = newMongoConnection()
	db = client.test
	imdb = db.imdb

	results = imdb.find().sort("rating", -1).limit(10)

	dataToReturn = []
	didi = dict()

	for result in results:
		didi = {
			'itemID' : result['id'],
			'content' : result['des'],
			'rating' : result['rating']
		}
		dataToReturn.append(didi)

	return dataToReturn


# Get the movie with the movieID
def imdbMongoGetMovie(movieID):
	client = newMongoConnection()
	db = client.test
	imdb = db.imdb
	doc = imdb.find_one({'id' : movieID})
	client.disconnect()

	if doc:
		return doc
	else:
		return 'no movie'





def imdbMongoGetAllMovies():
	client = newMongoConnection()
	db = client.test
	imdb = db.imdb

	return imdb.find()





def mongoFindItemPred(itemID):
	
	client = newMongoConnection()
	db = client.test
	users = db.users

	# users que tem o pred movie ou pelo menos
	# um movie igual ao user
	# docs = users.find({"$or" : [{"itemID": itemID}, {"itemID": predMovie}]})
	docs = users.find({"itemID": itemID})
	# docsPredMovie = users.find({"itemID": predMovie})
	client.disconnect()

	returnData = []
	# users que tem pelo menos um movie igual 
	# ao do user, e tem o predMovie
	for doc in docs:
		if doc['userID'] not in returnData: 
			returnData.append(doc['userID'])
	
	return returnData






