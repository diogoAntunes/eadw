from pymongo import MongoClient

client = MongoClient('localhost', 27017)

def mongoInsert(data):

	
	db = client.test
	imdb = db.imdb
	imdb.insert(data)


def mongoFindMovie(movieName):

	db = client.test
	imdb = db.imdb

	doc = imdb.find_one({"title": movieName})

	if doc.count() != 0:
		return doc

