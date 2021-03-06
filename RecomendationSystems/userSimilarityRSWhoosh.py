from whoosh.index import open_dir
from whoosh.qparser import  *
import re
import math
import operator

def sim(a, b, userMovies, predict, rA):

	ix = open_dir("indexdir")
	ratesA = userMovies # movieID : raiting
	ratesB = dict()		# movieID : raiting

	with ix.searcher() as searcher:
		query = QueryParser("userID",ix.schema,group=OrGroup).parse(b)
		results = searcher.search(query,limit=10000)
		for r in results:
			ratesB[r['itemID']] = r['rating'] 
	
	#print b
	#print ratesB
	#print a
	#print ratesA
	keys_a = set(ratesA.keys())
	keys_b = set(ratesB.keys())
	
	nRatingsB = len(keys_b)		#number of items rated by B

	intersection = keys_a & keys_b
	#print "Items comuns entre os dois users: "
	#print intersection
	#print len(intersection)


	#VARIAVEIS PARA CALCULO DA SIMILARIDADE
	SomaP = 0 		#set of items, rated both by a and b	
	Rbp = 0			#rating of user b for item p
	rB = 0			# user B average ratings

	#CALCULO AVERAGE RATINGS
	contador = 0

	for item in ratesB.keys():
		contador += ratesB[item]

	rB = float(contador)/nRatingsB

	#CALCULO SOMATORIO P	
	RateInA = 0
	RateInB = 0
	SomatorioRateInA_B = 0

	#print intersection
	for item in intersection:
		SomatorioRateInA_B += ((ratesA[item] - rA) * (ratesB[item] - rB))
		RateInA += ((ratesA[item] - rA)*(ratesA[item] - rA))
		RateInB += ((ratesB[item] - rB)*(ratesB[item] - rB))

	RateInA = math.sqrt(RateInA)
	RateInB = math.sqrt(RateInB)
	
	if((RateInA*RateInB) != 0):
		Similaridade = ((SomatorioRateInA_B)/(RateInA * RateInB))
	else:
		Similaridade = 0
	
	#RATING ITEM PARA PREDICTION POR ESTE USER B
	Rbp = ratesB[predict]

	return Similaridade, Rbp, rB


#CALCULO PARA PREDICTION
def pred(user, prediction):

	user = str(user)
	ix = open_dir("indexdir")
	userMovies = dict()		#dicionario com os items rated e rating do user escolhido
	sameMovies = dict()		#dicionario de users com pelo menos 1 item rated igual ao user escolhido
	countUsers = dict()
	predictionUsers = []
	chosenUsers = []
	chosenUsersFinal = []

	with ix.searcher() as searcher:
		query = QueryParser("userID",ix.schema,group=OrGroup).parse(user)
		results = searcher.search(query,limit=400)

		for r in results:
			userMovies[r['itemID']] = r['rating']

		for item in userMovies.keys():
			a = str(item)
			query = QueryParser("itemID",ix.schema,group=OrGroup).parse(a)
			results = searcher.search(query,limit=10000)
			
			sameMovies[a] = []
			for r in results:
				sameMovies[a].append(r['userID'])

		#PROCURAR NOS USERS SE TEM O ITEM QUE O CLIENTE QUER SABER O RATING
		query = QueryParser("itemID",ix.schema,group=OrGroup).parse(str(prediction))
		results = searcher.search(query,limit=10000)
		for r in results:
			predictionUsers.append(r['userID'])

	#VERIFICAR NUMERO DE ITEMS RATED EM COMUM ENTRE UTILIZADOR ESCOLHIDO E RESTANTES
	for item in sameMovies:
		for valor in sameMovies[item]:
			if valor in countUsers.keys():
				countUsers[valor] += 1
			else:
				countUsers[valor] = 1
	
	#APENAS ESCOLHER OS QUE TEM 10 OU MAIS ITEMS RATED EM COMUM
	for item in countUsers:
		if (countUsers[item] >= 10):
			chosenUsers.append(item)

	#SELECIONAR APENAS OS USERS QUE DERAM RATE AO ITEM QUE O UTILIZADOR ESCOLHIDO AINDA NAO PONTUOU
	for item in chosenUsers:
		if item in predictionUsers:
			chosenUsersFinal.append(item)

	flag = len(chosenUsersFinal)

	#VARIAVEIS PARA PREDICTON
	SomatorioCima = 0
	SomatorioBaixo = 0
	
	ratesA = userMovies
	keys_a = set(ratesA.keys())
	nRatingsA = len(keys_a)		#number of items rated by A
	contador = 0
	for item in ratesA.keys():
		contador += ratesA[item]

	rA = float(contador)/nRatingsA

	#FORMULA PARA PREDICTION PRED(A,P)
	for item in chosenUsersFinal:
		Similaridade, Rbp, rB = sim(user, str(item), userMovies, prediction, rA)
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

	# print predP

	if (predP > 5):
		predP = 5
		
	predReturn = round(predP)
	predReturn = int(predReturn)

	if (predReturn == 0):
		predReturn = 1

	return predReturn
	#print "PREDICTON PARA ITEM: " + str(prediction) + " = " + str(predReturn)
	#print userMovies

#pred(3, 258)