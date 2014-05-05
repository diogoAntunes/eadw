from pymongo import MongoClient
import simplejson
import json

# Insert a JSON document in the database
def mongoInsertJSON():

	client = MongoClient('localhost', 27017)	
	db = client.test
	imdb = db.imdb
	fd = open('populateData', 'r')
	text = fd.read()
	fd.close()
	returndata = {}
	returndata = simplejson.loads(text)
	imdb.insert(returndata)