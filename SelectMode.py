from testingSystem import *
import sys
sys.path.append('./RecomendationSystems')
from genderRS import *
from imdbRS import *
from userSimilarityRSMongoDB import *
from userSimilarityRSWhoosh import *
from recomendationSystem import *
sys.path.append('./DatabaseTools')
from DatabaseTools import *

def testSystem():
	
	sys.path.append('./Settings')
	file = open("u1.test")

	#ix = open_dir("indexdir")
	#schema = Schema(userID = NUMERIC(stored=True), itemID = NUMERIC(stored=True), rating = NUMERIC(stored=True))

	resultsPred = []
	resultsCorrect = []
	i = 0
	Somatorio = 0

	for line in file:

		#writer = ix.writer()
		doc = re.split('\W+', line)	
		userID = int(doc[0])
		itemID = int(doc[1])
		rating = int(doc[2])
		possibleRating = pred(userID, itemID)
		resultsPred.append(possibleRating)
		resultsCorrect.append(rating)
		Somatorio += abs(resultsPred[i] - resultsCorrect[i])
		#writer.add_document(userID=userID, itemID=itemID, rating=rating)
		#writer.commit()

		print "PREDICTION = " + str(possibleRating) + "	 CORRECT RATING = " + str(rating) + "	Somatorio = " + str(Somatorio) + "	  I = " + str(i)
		i += 1 


	MAE = 0			#MEAN ABSOLUTE ERROR
	Somatorio = 0
	i = 0
	Certos = 0
	Errados = 0

	for item in resultsPred:
		Somatorio += abs(resultsPred[i] - resultsCorrect[i])
		if(resultsPred[i] == resultsCorrect[i]):
			Certos += 1
		else:
			Errados += 1
		i += 1

	MAE = (float(Somatorio)/i)
	print MAE
	print Somatorio
	print i

	print "MEAN ABSOLUTE ERROR = " + str(MAE)
	print "CERTOS = " + str(Certos)
	print "ERRADOS = " + str(Errados)


def selectMode():
	
	print "Select the mode you want to run the system in: "
	print "\n"
	print "1 - Online Mode"
	print "2 - Batch Training Mode"
	print "3 - Batch Testing Mode"
	print "\n"

	try:
		mode=int(raw_input('Type in the number of the mode you want to select:'))
	except ValueError:
		mode=5
	
	return mode

def onMode():

	try:
		userID=int(raw_input('Type in your User ID: '))
	except ValueError:
		print"User ID not valid"

	#print userID
	#chamar recomendacao de movies
	#gerar classificacao para estes movies
	itemID, rating, title, itemID2, rating2, title2 = recomendMovie(userID)
	print 'Recomended Movies: '
	print '1)'
	print 'Movie ID: ', itemID
	print 'Title: ', title
	print 'Rating: ', rating
	print '2)'
	print 'Movie ID: ', itemID2
	print 'Title: ', title2
	print 'Rating: ', rating2

def TrainMode():

	ficheiro=raw_input('Type in the File Name to Create the Model: ')
	
	print 'Training Please Wait... '
	mongoPopulateUsers()
	print 'Done'


def TestMode():

	print 'Testing Please Wait... '
	testSystem()
	print 'Done'



md = selectMode()

if (md <= 3 & md >= 1):
	if (md == 1):
		print "Online Mode"
		onMode()

	if (md == 2):
		print "Batch Training Mode"
		TrainMode()

	if (md == 3):
		print "Batch Testing Mode"

else:
	print "The input is not a valid number! Select a value between 1 and 3."