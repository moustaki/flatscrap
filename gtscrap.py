#!/usr/bin/python
import urllib
import sys
from BeautifulSoup import BeautifulSoup

print "Scrapping "+sys.argv[1]

f = urllib.urlopen(sys.argv[1])
html = f.read()
f.close()

soup = BeautifulSoup(html)

def clean(atom):
        t1 = ''.join(atom.rsplit('&nbsp;'))
        t2 = ''.join(t1.rsplit('\n'))
        return t2


# Now, let's scrap!

location = clean(soup('span','location')[0].contents[1])
title = clean(soup('div',id="title")[0].contents[0].contents[0])
description = soup('div',id="desc")[0].contents[0].contents[0].contents[0]
email1 = soup('span','email')[0].contents[2].attrs[0][1]
if email1.startswith('/cgi-bin'):
	email = "http://www.gumtree.com"+email1
else :
	email = email1
image = "http://www.gumtree.com"+soup('div',id="images")[0].contents[1].attrs[0][1]


#tel = clean(soup('div',id="replyto")[0].contents[0].contents[3])


print location
print title
print description
print email
print image

