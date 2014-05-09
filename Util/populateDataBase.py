from pymongo import MongoClient
import simplejson
import json
import re

# Insert a JSON document in the database
def mongoInsertJSON():

	client = MongoClient('localhost', 27017)	
	db = client.test
	imdb = db.imdb
	fd = open('back', 'r')
	text = fd.read()
	fd.close()
	returndata = {}
	returndata = simplejson.loads(text)
	imdb.insert(returndata)

# {
# 	userID : id,
# 	movies : [{
# 		movieID : rating
# 	}]
# 		
# }
def mongoPopulateUsers():
	client = MongoClient('localhost', 27017)	
	db = client.test
	users = db.users

	# file = open("u.data")
	file = open("u1.base")

	# 196	242	3	881250949
	# user id | item id | rating | timestamp
	for line in file:
		doc = re.split('\W+', line)	
		userID = int(doc[0])
		itemID = int(doc[1])
		rating = int(doc[2])

		users.update({'userID' : userID},{
			"$push": { 'movies' : {'itemID' : itemID, 'rating' : rating} }
   	}, True)
		

def mongoTesteADD(userID, itemID, rating):
	client = MongoClient('localhost', 27017)	
	db = client.test
	users = db.users

	newUser = {'userID' : userID, 'itemID' : itemID, 'rating' : rating }
	users.insert(newUser)

mongoInsertJSON()