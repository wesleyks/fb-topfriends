# fb.py
#
# Wesley K Sun
#
# Script that lists your friends in some kind of order, probably ranked by amount of interactions
# It still has issues with dealing with unicode
#

import urllib2
import string
import mmap
import json
import sys
import re
import os
import getpass
import cookielib

ids = None
class Facebook():
	def __init__(self):
		self.email = raw_input("Facebook email address: ")
		self.password = getpass.getpass()
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.addheaders =  [('Referer', 'http://login.facebook.com/login.php'),
                            ('Content-Type', 'application/x-www-form-urlencoded'),
                            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')]
        	self.opener = opener
        def login(self):
        	url = 'https://login.facebook.com/login.php?login_attempt=1'
        	data = data = "locale=en_US&non_com_login=&email="+self.email+"&pass="+self.password+"&lsd=20TOl"
        	print "connecting to facebook...\n"
        	usock = self.opener.open('http://www.facebook.com')
       		print "inputting your data...\n"
        	usock = self.opener.open(url, data)
        	
        	a = usock.read()
		if "logout" in a:
			print "login successful!"
			return a
		else:
			print "login failed!  sorry...\n"
			print usock.read()
			sys.exit()
# some stupid code to find and parse the array of friend id's
f = Facebook()  #gets the Facebook class setup
a = f.login()	#should return the html data from facebook

map = mmap.mmap(a.fileno(), 0)
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

#query the facebook graph api
for i in range(len(ids)):
	url = "https://graph.facebook.com/" + ids[i] + "?fields=name"
	try:
		request = urllib2.urlopen(url)
		jstring = request.read()
		obj = json.loads(jstring)
		print str(i+1) + ":\t" + obj['name']
	except urllib2.HTTPError, e:
		print "Error code " + str(e.code) + " when getting user " + ids[i] + " Reason: " + e.read()