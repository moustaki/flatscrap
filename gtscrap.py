#!/usr/bin/python
import urllib
import sys
from BeautifulSoup import BeautifulSoup

print "Scrapping "+sys.argv[1]

f = urllib.urlopen(sys.argv[1])
html = f.read()
f.close()

soup = BeautifulSoup(html)

# Now, let's scrap!

location =  soup('span','location')[0].contents[1][6:]
title = soup('div',id="title")[0].contents[0].contents[0]
description = soup('div',id="desc")[0].contents[0].contents[0].contents[0]

print location
print title
print description


