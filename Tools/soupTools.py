import sys
import re
import urllib
import urlparse

from mechanize import Browser
from BeautifulSoup import BeautifulSoup

# urllib used to set http headers
class MyOpener(urllib.FancyURLopener):
	version = 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.2.15) Gecko/20110303 Firefox/3.6.15'

# Parse imdb page to fetch rating of movies
def getRatings(url):

	# url = 'http://us.imdb.com/M/title-exact?Moighty%20Aphrodite%20(1995)'
	try:
		br = Browser()
		br.set_handle_robots(False)
		br.open(url)

		if re.search(r'/title/tt.*', br.geturl()):
			soup = BeautifulSoup(MyOpener().open(url).read())
		else:
			link = br.find_link(url_regex = re.compile(r'/title/tt.*'))
			res = br.follow_link(link)
			soup = BeautifulSoup(res.read())
		 
		# movie_title = soup.find('title').contents[0]
		# des = soup.find('meta',{'name':'description'})['content']
		
		rate = soup.find('span',itemprop='ratingValue')
	except:
		print 'Error no rating'
		rating = str(0)
	else:
		if rate:
			rating = str(rate.contents[0])
		else:
			rating = str(0)
			print 'No rate'
	 

	return rating

# Saves Ratings of Movie to JSON file
def moviesRatingToDB():

	f = open("./Util/u.item", "r")
	finalInsert = []

	movies = dict()
	for movie in f:
		movieParsed = movie.split("|")
		rate = getRatings(movieParsed[4])
		movies = ({"title" : movieParsed[1].encode('utf-8'), "rating" : rate})
		finalInsert.append(movies)
		print movieParsed[0]
		try:
			jsondata = simplejson.dumps(finalInsert, indent=4, skipkeys=True, sort_keys=True)
			fd = open('json.txt', 'w')
			fd.write(jsondata)
			fd.close()
		except:
			print 'ERROR writing', filename
			pass


# getRatings('http://us.imdb.com/M/title-exact?Yinshi%20Nan%20Nu%20(1994)')
# getRatings('http://us.imdb.com/M/title-exact?Mighty%20Aphrodite%20(1995)')