import imdb

access = imdb.IMDb()
movie = access.get_movie(1132626)

print "title: %s year: %s" % (movie['title'], movie['year'])
print "Cover url: %s" % movie['cover url']