import re
from userSimilarity import *

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
	possibleRating = pred(userID, itemID)
	resultsPred.append(possibleRating)
	resultsCorrect.append(rating)
	print "PREDICTION = " + str(possibleRating)


MAE = 0			#MEAN ABSOLUTE ERROR
Somatorio = 0
i = 0

for item in resultsPred:
	Somatorio += abs(resultsPred[i] - resultsCorrect[i])
	i += 1

MAE = (Somatorio/i)

print "MEAN ABSOLUTE VALUE = " + str(MAE)