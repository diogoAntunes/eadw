import imdb
from pprint import pprint
from rottentomatoes import RT

# API KEY ROTTEN TOMATOES: 
# swkke96gu5rwqtrqakdewbgs

# put imdb relevant data in database
# query from db

def imdbSearch(title):

	# r = RT('swkke96gu5rwqtrqakdewbgs')
	# result = r.search(title)[0]
	# if 'alternate_ids' in result.keys():
		# imdbID = result['alternate_ids']['imdb']

	ia = imdb.IMDb()
	searchResult = ia.search_movie(title)[0]
	imdbID = searchResult.movieID
	s_result = ia.get_movie(imdbID)	
	keys = s_result.keys()
		
	dataToDB = dict()
	dataToDB["keywords"] = []
	for keyword in ia.get_movie_keywords(imdbID)['data']['keywords'][:10]:
		dataToDB["keywords"].append(str(keyword))

	if 'plot outline' in keys:
		dataToDB["plot outline"] = s_result['plot outline'].encode('utf-8')
	if 'title' in keys:
		dataToDB["title"] = s_result['title'].encode('utf-8')
	if 'rating' in keys:
		dataToDB["rating"] = s_result['rating']
	if 'producer' in keys:
		dataToDB["producer"] = []
		for producer in s_result['producer']:
			dataToDB["producer"].append(producer['name'].encode('utf-8'))
	if 'director' in keys:
		dataToDB["director"] = []
		for director in s_result['director']:
			dataToDB["director"].append(director['name'].encode('utf-8'))
	if 'cast' in keys:
		dataToDB["cast"] = []
		for actor in s_result['cast']:
			dataToDB["cast"].append(actor['name'].encode('utf-8'))

	# pprint(dataToDB)
	# pprint(keys)
	# pprint(s_result['cast'])
	# pprint(s_result['actors'])
	# mongoInsert(dataToDB)


def moviesRating(movieName):

	ia = imdb.IMDb()
	searchResult = ia.search_movie(movieName)[0]
	imdbID = searchResult.movieID
	
	try:
		s_result = ia.get_movie(imdbID)	
		keys = s_result.keys()

		if 'rating' in keys:
			return s_result['rating']
	except:
		print 'No Rate'
		return 3

def imdbGetMovieURL(movieName):
	ia = imdb.IMDb()
	searchResult = ia.search_movie(movieName)[0]
	url = ia.get_imdbURL(searchResult)
	
	return url
	

# imdbGetMovie('Gladiator', 2)