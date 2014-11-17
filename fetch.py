# 
# @author Apan Qasem
# @date 10/15/14
#    
# This program collects data via the Twitter search API and generates an HTML file. 
# Search results are filtered by geo-tagging.
# 
# The HTML file contains coordinates and text of each filtered result 
# The generated HTML file is concatenated with another file that contains the visiualization script
# 
# 

import oauth2 as oauth        # oauth authorization needed for twitter API
import json                   # converting data into json object 
from pprint import pprint     # pretty print 
import os                     # for contatenating generated files 
import sys

# my keys, need all four of them 
consumer_key = "sBLybxUMOi7P23wdP5QFVn2tv"
consumer_secret = "n1OSCM3mXyG9LVEJ7fbVMFzECjgHvre0kpibTjuSPozGcRjWTF"
token_key = "423210116-BCgCthEfEA2QRSTnDJ5tYcbt3qGQp2qjEOd1ihJB"
token_secret = "RDJWXbg8pVPgJRTJTzUJy1jilpchdFsL203h8273bIZlR"

#
# function to construct search url 
#   - count value is always set to 100 
#   - defaul value for max_id is 0
#
def makeurl(searchterm, max_id=0) :
    baseurl = "https://api.twitter.com/1.1/search/tweets.json"
    count = "100"
    if max_id == 0:
        url = baseurl + '?q=' + searchterm + '&' \
              + 'count=' + count    
    else:
        url = baseurl + '?q=' + searchterm + '&' \
              + 'max_id=' + str(max_id) + '&' \
              + 'count=' + count    
    return url 

#
# Following functions generates HTML output 
#

#
# start tr element and write longitude and latitude in two table cells 
# 
def write_coord(lng, lat, num, localfile) :
    localfile.write("<tr id = \"coord" + str(num) + "\">\n")
    localfile.write("<td id = \"lng\"" + ">")
    localfile.write(str(lng))
    localfile.write("</td>")
    localfile.write("<td id = \"lat\"" + ">")
    localfile.write(str(lat))
    localfile.write("</td>\n")
    return 

#
# write tweet text and end tr element 
#
def write_text_as_td(text):
    localfile.write("<td>")
    localfile.write(text)
    localfile.write("</td>\n")
    localfile.write("</tr>\n")
    return 

#
# start html body and write div element for map 
# 
def write_html_body_prefix(localfile) :
    localfile.write("<body>\n")
    localfile.write("<div id = \"map\" style=\"height: 468px\"></div></div>")
    localfile.write("<table id = \"cTable\">\n")
    return 
#
# end table element 
# end body
#
def write_html_body_suffix(localfile) :
    localfile.write("</table>\n")
    localfile.write("</body>\n")
    return 
    
# construct search term 
searchTerm = "acl AND diplo"

# short name used as file prefix 
searchTermShort = "acl"

url = makeurl(searchTerm)

# set up oauth tokens
token = oauth.Token(token_key, token_secret)
consumer = oauth.Consumer(consumer_key, consumer_secret)

# create client and request data 
client = oauth.Client(consumer, token)

# determine loop count 
MAX_RESULTS_FROM_TWITTER = 100
desired_max_count = 10000
loopcount = desired_max_count / MAX_RESULTS_FROM_TWITTER 


# output HTML file for coords 
filename = searchTermShort + '_tweets_coords.html'
localfile = open(filename, 'w');


write_html_body_prefix(localfile)

coord_count = 0
for i in range(loopcount):
    header, contents = client.request(url, method="GET")
    data = json.loads(contents)

    results = len(data['statuses'])    
    for j in range(results):
        if data['statuses'][j]['coordinates'] != None :
            coords = data['statuses'][j]['coordinates'].values()[1]
            lng = coords[0]
            lat = coords[1]
            write_coord(lng, lat, coord_count, localfile)
            tweet_text = data['statuses'][j]['text']
            
            # need unicode encoding for tweet text 
            write_text_as_td(tweet_text.encode('utf8'))
            coord_count = coord_count + 1

    if results < 100:
        break

    next_id = data['statuses'][results - 1]['id']
    oldest_tweet_date = data['statuses'][results - 1]['created_at']
    url = makeurl(searchTerm, next_id)

write_html_body_suffix(localfile)

# done generating all output, close file 
localfile.close()

# use OS system call to concatenate generated file (HTML <body>) with file containing 
# JavaScript with calls to Google Maps API
viz_file_name = searchTermShort + '_tweets_map.html'
cat_command = "cat viz_script_marker.html " + filename + " > "  + viz_file_name
os.system(cat_command)
