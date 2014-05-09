from pymongo import MongoClient
import simplejson
import re

# Insert a JSON document in the database
def mongoInsertJSON():

	# Connection to dataBase
	client = MongoClient('localhost', 27017)	
	db = client.test
	imdb = db.imdb

	fd = open('./DataBaseTools/populateData', 'r')

	text = fd.read()
	fd.close()
	
	returndata = {}
	returndata = simplejson.loads(text)
	
	imdb.insert(returndata)


# Populates the dataBase with items of the 
# following format:
# 
# {
# 	'userID' : id,
# 	'movies' : [{
# 		'itemID' : movieID,
# 		'rating' : rating
# 	}]		
# }
def mongoPopulateUsers():
	
	# Connection to dataBase
	client = MongoClient('localhost', 27017)	
	db = client.test
	users = db.users

	file = open("./Settings/u1.base")

	for line in file:
		doc = re.split('\W+', line)	
		userID = int(doc[0])
		itemID = int(doc[1])
		rating = int(doc[2])

		# Insertion in the dataBase
		users.update({'userID' : userID},{
			"$push": { 'movies' : {'itemID' : itemID, 'rating' : rating} }
   	}, True)