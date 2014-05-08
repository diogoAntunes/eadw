import re
from userSimilarityWhoosh import *
from eadw import *
from whoosh.index import create_in
from whoosh.fields import *
from whoosh.qparser import QueryParser
import os

file = open("u1.test")
ix = open_dir("indexdir")
schema = Schema(userID = NUMERIC(stored=True), itemID = NUMERIC(stored=True), rating = NUMERIC(stored=True))

resultsPred = []
resultsCorrect = []
i=0

for line in file:
	writer = ix.writer()
	doc = re.split('\W+', line)	
	userID = int(doc[0])
	itemID = int(doc[1])
	rating = int(doc[2])
	possibleRating = int(pred(userID, itemID))
	#possibleRating = getPrediction(itemID, userID)
	resultsPred.append(possibleRating)
	resultsCorrect.append(rating)

	writer.add_document(userID=userID, itemID=itemID, rating=rating)
	writer.commit()
	
	print "PREDICTION = " + str(possibleRating) + "      CORRECT RATING --------->" + str(rating) + " I = " + str(i)
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
