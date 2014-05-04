from pymongo import MongoClient

def mongoInsert(data):

	client = MongoClient('localhost', 27017)
	db = client.test
	imdb = db.imdb
	imdb.insert(data)
