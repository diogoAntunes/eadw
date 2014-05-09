from eadw import *


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
	print ficheiro


#def TestMode():


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