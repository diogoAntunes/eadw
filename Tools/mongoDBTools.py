from pymongo import MongoClient

client = MongoClient('localhost', 27017)


# Create Class

def mongoInsert(data):

	db = client.test
	imdb = db.imdb
	imdb.insert(data)
	client.disconnect()

def mongoFindMovie(movieName):

	db = client.test
	imdb = db.imdb

	doc = imdb.find_one({"title": movieName})
	client.disconnect()

	if doc:
		return doc['rating']

# xpto = mongoFindMovie("Devil's Own, The (1997)")
# print xpto['rating']
