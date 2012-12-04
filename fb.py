# fb.py
#
# Wesley K Sun
#
# David Tuber
#
# Script that lists your friends in some kind of order, probably ranked by amount of interactions
# It still has issues with dealing with unicode
#

import urllib2, cookielib, re, os, sys, getpass, string, json

class Facebook():
	def __init__(self):
		self.email = raw_input("What's your email? ")
		self.password = getpass.getpass()
		cj = cookielib.CookieJar()
		opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
		opener.addheaders = [('Referer', 'http://login.facebook.com/login.php'),
                            ('Content-Type', 'application/x-www-form-urlencoded'),
                            ('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.1.7) Gecko/20091221 Firefox/3.5.7 (.NET CLR 3.5.30729)')]
	
		self.opener = opener
		
	def login(self):

		url = 'https://login.facebook.com/login.php?login_attempt=1'
		data = "locale=en_US&non_com_login=&email="+self.email+"&pass="+self.password+"&lsd=20TOl"
		usock = self.opener.open('http://www.facebook.com')

		usock = self.opener.open(url, data)

		a = usock.read()
		if "logout" in a:
			print "Logged in."
			return a
		else:
			print "failed login"
			print usock.read()
			sys.exit()
f = None
a = None
if len(sys.argv) > 1:
	with open(sys.argv[1],'r') as f:
		a = f.read()
else:
	f = Facebook()
	a = f.login()

start = a.find('OrderedFriendsListInitialData')
start = a.find('list', start)
start = a.find('[', start) + 1
end = a.find(']', start)

#a.seek(start)

idstring = a[start:end]
idstring = idstring.translate(None, '\n"')
ids = idstring.split(',')

print "Number of entries: " + str(len(ids))

for i in range(len(ids)):
	url = "https://graph.facebook.com/"+ids[i]+"?fields=name"
	try:
		request = urllib2.urlopen(url)
		jstring = request.read()
		obj = json.loads(jstring)
		print str(i+1) + ":\t" + obj['name']
	except urllib2.HTTPError, e:
		print "Error code " + str(e.code) + " when getting user " + ids[i] + " Reason: " + e.read()
