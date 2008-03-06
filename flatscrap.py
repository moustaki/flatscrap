#!/usr/bin/python
import urllib
import sys
from BeautifulSoup import BeautifulSoup
from geopy import geocoders
from rdflib import ConjunctiveGraph
from rdflib import BNode, Literal, Namespace, URIRef
from rdflib import plugin
from rdflib.syntax.serializers import TurtleSerializer

#print "Scrapping "+sys.argv[1]

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
try:
	image = "http://www.gumtree.com"+soup('div',id="images")[0].contents[1].attrs[0][1]
except:
	image = ''

#tel = clean(soup('div',id="replyto")[0].contents[0].contents[3])

# Geocoding
g = geocoders.Google('ABQIAAAAu0AMQcAkvqfViJpEeSH_-hT2yXp_ZAY8_ufC3CFXhHIE1NvwkxQ0_Z6CDgX2Q08wvAh1aYjckybfeA')
place, (lat,lng) = g.geocode(location)


#print "Location: " + location
#print "Title: " + title
#print "Description: " + description
#print "Email: "+email
#print "Image: "+image


RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
GT = Namespace("http://purl.org/ontology/flat/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DC = Namespace("http://purl.org/dc/elements/1.1/")
WGS = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
graph = ConjunctiveGraph()

flat = URIRef("#flat")
p = BNode()
e = URIRef(email)
i = URIRef(image)

graph.add((flat,RDF.type,GT['Flat']))
graph.add((flat,FOAF['based_near'],p))
graph.add((p,RDFS.label,Literal(place)))
graph.add((p,DC['title'],Literal(location)))
graph.add((p,WGS['lat'],Literal(lat)))
graph.add((p,WGS['long'],Literal(lng)))
graph.add((flat,FOAF['mbox'],e))
graph.add((flat,FOAF['depiction'],i))
graph.add((flat,DC['title'],Literal(title)))
graph.add((flat,DC['description'],Literal(description)))

print graph.serialize(destination=sys.argv[2],format='xml')

