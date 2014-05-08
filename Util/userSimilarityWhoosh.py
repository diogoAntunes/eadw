from whoosh.index import open_dir
from whoosh.qparser import  *
import re
from pprint import pprint
import math
import sys
sys.path.append('../Tools')
from mongoDBTools import *

def sim(a, b, userMovies, predict):

	# ix = open_dir("indexdir")
	ratesA = userMovies # movieID : raiting
	ratesB = userMongoGetUser(b)

	# print ratesB

	#print b
	#print ratesB
	#print a
	#print ratesA

	keys_a = set(ratesA.keys())
	keys_b = set(ratesB.keys())
	
	nRatingsA = len(keys_a)		#number of items rated by A
	nRatingsB = len(keys_b)		#number of items rated by B

	intersection = keys_a & keys_b
	#print "Items comuns entre os dois users: "
	#print intersection
	#print len(intersection)


	#VARIAVEIS PARA CALCULO DA SIMILARIDADE
	SomaP = 0 		#set of items, rated both by a and b	
	Rbp = 0			#rating of user b for item p
	rA = 0			# user A average ratings
	rB = 0			# user B average ratings

	#CALCULO AVERAGE RATINGS
	contador = 0
	
	for item in ratesA.keys():
		contador += ratesA[item]

	rA = contador/nRatingsA
	
	contador = 0

	for item in ratesB.keys():
		contador += ratesB[item]

	rB = contador/nRatingsB

	#CALCULO SOMATORIO P	
	contador = 0
	RateInA = 0
	RateInB = 0
	SomatorioRateInA_B = 0

	for item in intersection:
		SomatorioRateInA_B += ((ratesA[item] - rA) * (ratesB[item] - rB))
		RateInA += ((ratesA[item] - rA)*(ratesA[item] - rA))
		RateInB += ((ratesB[item] - rB)*(ratesB[item] - rB))

	RateInA = math.sqrt(RateInA)
	RateInB = math.sqrt(RateInB)

	Similaridade = ((SomatorioRateInA_B)/(RateInA * RateInA))
	
	#RATING ITEM PARA PREDICTION POR ESTE USER B
	# print ratesB[predict]
	Rbp = ratesB[predict]

	#print "SIMILARIDADE: "
	#print Similaridade

	return Similaridade, Rbp, rA, rB


#CALCULO PARA PREDICTION
def pred(user, prediction):

	userMovies = userMongoGetUser(user)	#dicionario com os items rated e rating do user escolhido
	sameMovies = dict()		#array de users com pelo menos 1 item rated igual ao user escolhido
	countUsers = dict()
	predictionUsers = dict()
	chosenUsers = []
	chosenUsersFinal = []

	for movie in userMovies.keys():
		sameMovies = mongoFindItem(movie, sameMovies)
	
	# print sameMovies
	#PROCURAR NOS USERS SE TEM O ITEM QUE O CLIENTE QUER SABER O RATING
	predictionUsers = mongoFindItemPred(prediction)

	#VERIFICAR NUMERO DE ITEMS RATED EM COMUM ENTRE UTILIZADOR ESCOLHIDO E RESTANTES
	# sameMovies = ['userID', 'userID', 'userID'...]
	# ids de users que tem pelo menos um dos filmes do user
	# for item in sameMovies:
	# 	if item in countUsers.keys():
	# 		countUsers[item] += 1
	# 	else:
	# 		countUsers[item] = 1
	
	#APENAS ESCOLHER OS QUE TEM 15 OU MAIS ITEMS RATED EM COMUM
	for item in sameMovies.keys():
		if (sameMovies[item] >= 15):
			chosenUsers.append(item)

	#SELECIONAR APENAS OS USERS QUE DERAM RATE AO ITEM QUE O UTILIZADOR ESCOLHIDO AINDA NAO PONTUOU
	for item in chosenUsers:
		if item in predictionUsers:
			chosenUsersFinal.append(item)

	flag = len(chosenUsersFinal)
	#print "FLAGGGGG"
	#print flag

	#VARIAVEIS PARA PREDICTON
	SomatorioCima = 0
	SomatorioBaixo = 0
	rA = 0

	#FORMULA PARA PREDICTION PRED(A,P)
	for item in chosenUsersFinal:
		Similaridade, Rbp, rA, rB = sim(user, item, userMovies, prediction)
		if (flag > 9):
			if (Similaridade >= 0.5):
				SomatorioCima += (Similaridade * (Rbp - rB))
				SomatorioBaixo += Similaridade
		else:
			SomatorioCima += (Similaridade * (Rbp - rB))
			SomatorioBaixo += Similaridade


	predP = (rA + (SomatorioCima/SomatorioBaixo))

	return predP
	#print "PREDICTON PARA ITEM: " + str(prediction) + " = " + str(predP)
	#print userMovies

#pred(3, 65)