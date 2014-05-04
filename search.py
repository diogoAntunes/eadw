from whoosh.index import open_dir
from whoosh.qparser import  *
import re

# Rating looking at the genres

# Convert to unicode
ix = open_dir("indexdir")
userMovies = dict()
moviesGenre = dict()

# unknown | Action | Adventure | Animation |
# Childrens | Comedy | Crime | Documentary | 
# Drama | Fantasy | Film-Noir | Horror | 
# Musical | Mystery | Romance | Sci-Fi |Thriller | 
# War | Western |

with ix.searcher() as searcher:
    query = QueryParser("userID",ix.schema,group=OrGroup).parse("3")
    results = searcher.search(query,limit=100)
    for r in results:
        userMovies[r['itemID']] = r['rating'] 
       
    print userMovies

f = open("u.item", "r")

for movie in f:
    movieParsed = movie.split("|")
    movieID = int(movieParsed[0])
    if movieID in userMovies.keys():
        genres = movieParsed[5:]
        moviesGenre[movieID] = []
        for genre in genres:
            moviesGenre[movieID].append(int(genre))

# print moviesRating           
def rating(id):

    f = open("u.item", "r")
    movieFound = dict()
    # relevance = []
    relevance = dict()

    for movie in f:
        movieParsed = movie.split("|")
        movieID = int(movieParsed[0])
        if movieID == id:
            genres = movieParsed[5:]
            movieFound[movieID] = []
            for genre in genres:
                movieFound[movieID].append(int(genre))
    
    
    if len(movieFound.keys()) != 0:
        a = []
        print movieFound[id]
        for k, v in enumerate(movieFound[id]):
            if v == 1:
                a.append(k)
        lenA = len(a)
        for movie in moviesGenre:
            b = []
            for k, v in enumerate(moviesGenre[movie]):
                if v == 1:
                    b.append(k)
            intersect = len(set(a).intersection(set(b)))
            if lenA >=3:
                if intersect >= (len(a)-1):
                    # relevance.append(movie)
                    relevance[movie] = intersect
            else:
                if intersect >= lenA:
                    # relevance.append(movie)
                    relevance[movie] = intersect


    return relevance

rates = rating(353)
print rates

somRate = 0
somIntersect = 0
for rate in rates:
    somRate += userMovies[rate] * rates[rate]
    somIntersect += rates[rate]

total = float(somRate)/somIntersect
print total

av = 0
for rate in rates:
    av += userMovies[rate]

print float(av)/len(rates)