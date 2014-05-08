import re
from userSimilarity import *
from eadw import *

file = open("u1.test")
resultsPred = []
resultsCorrect = []

# 196	242	3	881250949
# user id | item id | rating | timestamp
for line in file:
	doc = re.split('\W+', line)	
	userID = int(doc[0])
	itemID = int(doc[1])
	rating = int(doc[2])
	possibleRating = int(pred(userID, itemID))
	#possibleRating = getPrediction(itemID, userID)
	resultsPred.append(possibleRating)
	resultsCorrect.append(rating)
	
	print "PREDICTION = " + str(possibleRating) + "      CORRECT RATING --------->" + str(rating)


MAE = 0			#MEAN ABSOLUTE ERROR
Somatorio = 0
i = 0

for item in resultsPred:
	Somatorio += abs(resultsPred[i] - resultsCorrect[i])
	i += 1

MAE = (float(Somatorio)/i)
print MAE
print Somatorio
print i

print "MEAN ABSOLUTE ERROR = " + str(MAE)