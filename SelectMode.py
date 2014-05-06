
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





md = selectMode()

if (md <= 3 & md >= 1):
	print "Sucess" #chamar funcao para arrancar o modo pretendido
else:
	print "The input is not a valid number! Select a value between 1 and 3."