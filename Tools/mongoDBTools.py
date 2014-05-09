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
	else:
		return 'no movie'

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


def imdbMongoSetRate(movieID, newRating):
	print 'UPDATING RATING'
	client = newMongoConnection()
	db = client.test
	imdb = db.imdb
	
	print 'MOVIE ID: ', movieID
	print 'NEW RATE : ', newRating

	imdb.update({"id" : movieID}, {"$set": {"rating" : newRating}})
	client.disconnect()


# USER MONGO TOOLS
def userMongoGetUser(userID):

# retorna dict() com:
# { movieID : rating }
	
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


def imdbMongoAddMovie(movieID, des, rating):
	print 'Adding Movie'
	print movieID, des, rating
	client = newMongoConnection()
	db = client.test
	imdb = db.imdb
	newMovie = {'id' : movieID, 'rating' : rating, 'des' : des}
	imdb.insert(newMovie)

	client.disconnect()

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

# print imdbMongoGetTopMovies()[0]