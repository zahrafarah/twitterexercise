# 
# Tasks 
#    - insert own key and access token 
#    - use a different search term 
#    - rename saved file 
#    - add one more search criteria
#        look at https://dev.twitter.com/rest/reference/get/search/tweets for options
#

import oauth2 as oauth        # oauth authorization needed for twitter API
import json                   # converting data into json object 
from pprint import pprint     # pretty print 
    

# construc search url
baseurl = "https://api.twitter.com/1.1/search/tweets.json"
searchterm = "texas+ebola"
count = "100"

url = baseurl + '?q=' + searchterm + '&' \
      + 'count=' + count

# my keys, need all four of them 
consumer_key = "sBLybxUMOi7P23wdP5QFVn2tv"
consumer_secret = "n1OSCM3mXyG9LVEJ7fbVMFzECjgHvre0kpibTjuSPozGcRjWTF"
token_key = "423210116-BCgCthEfEA2QRSTnDJ5tYcbt3qGQp2qjEOd1ihJB"
token_secret = "RDJWXbg8pVPgJRTJTzUJy1jilpchdFsL203h8273bIZlR"

# set up oauth tokens
token = oauth.Token(token_key, token_secret)
consumer = oauth.Consumer(consumer_key, consumer_secret)

# create client and request data 
client = oauth.Client(consumer, token)
header, contents = client.request(url, method="GET")

# write retrieved data to file 
filename = 'texas_tweets.json'
localfile = open(filename, 'w');
localfile.write(contents);

# convert to json object 
data = json.loads(contents)

# print meta data on search results 
pprint(data['search_metadata'])



