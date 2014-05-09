import re
import math
import sys
sys.path.append('./DataBaseTools')
from mongoDBTools import *

def sim(rA, rB, a, b, userMovies, predict):

	ratesA = userMovies # movieID : raiting
	ratesB = userMongoGetUser(b)

	keys_a = set(ratesA.keys())
	keys_b = set(ratesB.keys())
	
	nRatingsA = len(keys_a)		#number of items rated by A
	nRatingsB = len(keys_b)		#number of items rated by B

	intersection = keys_a & keys_b

	
	# Para os dois users ir buscar a intersection entre as keys()
	# Para cada um dos users calcular a media dos seus ratings
	# Agora apenas para os items na intersection
	# Para cada user subtrair o seu rate - a sua media

	RateInA = 0
	RateInB = 0
	SomatorioRateInA_B = 0
	Rbp = 0			#rating of user b for item p
	
	for item in intersection:
		SomatorioRateInA_B += ((ratesA[item] - rA) * (ratesB[item] - rB))
		RateInA += ((ratesA[item] - rA)*(ratesA[item] - rA))
		RateInB += ((ratesB[item] - rB)*(ratesB[item] - rB))

	RateInA = math.sqrt(RateInA)
	RateInB = math.sqrt(RateInB)

	Similaridade = ((SomatorioRateInA_B)/(RateInA * RateInB))
	Rbp = ratesB[predict]

	return Similaridade, Rbp


#CALCULO PARA PREDICTION
def pred(user, prediction):

	userMovies = userMongoGetUser(user)	#dicionario com os items rated e rating do user escolhido
	sameMovies = []		#array de users com pelo menos 1 item rated igual ao user escolhido
	countUsers = dict()
	predictionUsers = dict()
	chosenUsers = []
	chosenUsersFinal = []

	# utilizadores que tem pelo menos 1 item em comum com o userA
	for movie in userMovies.keys():
		sameMovies = mongoFindItem(movie, sameMovies, prediction)

	for item in sameMovies:
		if item in countUsers.keys():
			countUsers[item] += 1
		else:
			countUsers[item] = 1
	
	#APENAS ESCOLHER OS QUE TEM 10 OU MAIS ITEMS RATED EM COMUM
	for item in sameMovies:
		if (countUsers[item] >= 10):
			chosenUsers.append(item)

	flag = len(chosenUsers)
	
	#VARIAVEIS PARA PREDICTON
	SomatorioCima = 0
	SomatorioBaixo = 0
	rA = 0
	rA = mongoGetAVG(user)

	#FORMULA PARA PREDICTION PRED(A,P)
	for item in chosenUsers:	
		rB = mongoGetAVG(item)
		Similaridade, Rbp = sim(rA, rB, user, item, userMovies, prediction)
		if (flag > 9):
			if (Similaridade >= 0.5):
				SomatorioCima += (Similaridade * (Rbp - rB))
				SomatorioBaixo += Similaridade
		else:
			if(Similaridade >= 0):
				SomatorioCima += (Similaridade * (Rbp - rB))
				SomatorioBaixo += Similaridade

	if (SomatorioBaixo != 0):
		predP = (rA + (SomatorioCima/SomatorioBaixo))
	else:
		predP = 3

	if (predP > 5):
		predP = 5
		
	predReturn = round(predP)
	predReturn = int(predReturn)

	if (predReturn == 0):
		predReturn = 1

	return predReturn
	# print "PREDICTON PARA ITEM: " + str(prediction) + " = " + str(predP)
	# print userMovies