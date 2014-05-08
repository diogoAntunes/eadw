from pymongo import MongoClient

def newMongoConnection():
	client = MongoClient('localhost', 27017)
	return client

# IMDB MONGO TOOLS
def imdbMongoGetAllMovies():
	client = newMongoConnection()
	db = client.test
	imdb = db.imdb

	return imdb.find()

def imdbMongoGetMovie(movieID):
	client = newMongoConnection()
	db = client.test
	imdb = db.imdb
	doc = imdb.find_one({'id' : movieID})
	client.disconnect()

	if doc:
		return doc

def imdbMongoAddMovie(movieID, des, rating):
	client = newMongoConnection()
	db = client.test
	imdb = db.imdb
	newMovie = {
		"id" : movieID,
		"des" : des,
		"rating" : rating
	}
	imdb.insert(newMovie)
	client.disconnect()


def imdbMongoSetRate(movieID, newRating):
	print 'UPDATING RATING'
	client = newMongoConnection()
	db = client.test
	imdb = db.imdb
	
	imdb.update({"id" : movieID}, {"$set": {"rating" : newRating}})
	client.disconnect()


# USER MONGO TOOLS
def userMongoGetUser(userID):

# retorna dict() com:
# { movieID : rating }
	
	client = newMongoConnection()
	db = client.test
	users = db.users

	docs = users.find({"userID": userID})
	client.disconnect()

	userToReturn = dict()

	for doc in docs:
		userToReturn[doc['itemID']] = doc['rating']
	
	return userToReturn


def mongoFindItem(itemID, sameMovies):
	
	client = newMongoConnection()
	db = client.test
	users = db.users

	# users que tem o pred movie ou pelo menos
	# um movie igual ao user
	# docs = users.find({"$or" : [{"itemID": itemID}, {"itemID": predMovie}]})
	docs = users.find({"itemID": itemID})
	# docsPredMovie = users.find({"itemID": predMovie})
	client.disconnect()


	# users que tem pelo menos um movie igual 
	# ao do user, e tem o predMovie
	for doc in docs:
		if doc['userID'] in sameMovies.keys(): 
			sameMovies[doc['userID']] += 1
		else:
			sameMovies[doc['userID']] = 1
	
	return sameMovies

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


# imdbMongoGetAllMovies()