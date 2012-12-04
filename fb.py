import urllib2
import string
import mmap
import json
import sys

ids = None


# some stupid code to find and parse the array of friend id's
with open ('source.txt','r+') as f:
	map = mmap.mmap(f.fileno(), 0)
	start = map.find('OrderedFriendsListInitialData')
	start = map.find('list',start)
	start = map.find('[',start) + 1
	end = map.find(']',start)
	map.seek(start)
	#read the string and parse into array
	idstring = map.read(end-start)
	idstring = idstring.translate(None,'\n"')
	ids = idstring.split(',')

print "Number of entries: " + str(len(ids))

for i in range(len(ids)):
	url = "https://graph.facebook.com/" + ids[i] + "?fields=name"
	try:
		request = urllib2.urlopen(url)
		jstring = request.read()
		obj = json.loads(jstring)
		print str(i+1) + ":\t" + obj['name']
	except urllib2.HTTPError, e:
		print "Error code " + str(e.code) + " when getting user " + ids[i] + " Reason: " + e.read()