#!/usr/bin/python
import urllib
import sys
from BeautifulSoup import BeautifulSoup

print "Scrapping "+sys.argv[1]

f = urllib.urlopen(sys.argv[1])
html = f.read()
f.close()

soup = BeautifulSoup(html)

location =  soup('span','location')[0].contents[1][6:]

print location




