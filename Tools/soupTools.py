import sys
import re
import urllib
import urlparse
import unicodedata
import simplejson
import json

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
			print 'B'
			soup = BeautifulSoup(MyOpener().open(url).read())
		else:
			link = br.find_link(url_regex = re.compile(r'/title/tt.*'))
			res = br.follow_link(link)
			soup = BeautifulSoup(res.read())
		
		# movie_title = soup.find('title').contents[0]
		des = (soup.find('meta',{'name':'description'})['content']).encode('utf-8')
		rate = soup.find('span',itemprop='ratingValue')
		# print movie_title
		# print des
	except:
		print 'Error no rating'
		rating = str(0)
		des = ""
	else:
		if rate:
			rating = str(rate.contents[0])
		else:
			rating = str(0)
			print 'No rate'
	


	return rating, des

# Saves Ratings of Movie to JSON file
def moviesRatingToDB():

	f = open("u.item", "r")
	finalInsert = []

	movies = dict()
	for movie in f:
		movieParsed = movie.split("|")
		movieID = int(movieParsed[0])
		rate, des = getRatings(movieParsed[4])
		movies = ({
			"rating" : rate,
			"des" : des,
			"id" : movieID
			})
		finalInsert.append(movies)
		print movieParsed[0]
		try:
			jsondata = simplejson.dumps(finalInsert, indent=4, skipkeys=True, sort_keys=True)
			fd = open('json.txt', 'w')
			fd.write(jsondata)
			fd.close()
		except:
			print 'ERROR writing'
			pass

moviesRatingToDB()

# getRatings('http://us.imdb.com/M/title-exact?Mis%E9rables%2C%20Les%20%281995%29')
# getRatings('http://us.imdb.com/M/title-exact?Mighty%20Aphrodite%20(1995)')