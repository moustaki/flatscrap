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


class FlatScrape :

	def __init__(self,url) :
		self.url = url

        def __clean(self,atom):
                t1 = ''.join(atom.rsplit('&nbsp;'))
                t2 = ''.join(t1.rsplit('\n'))
                return t2


	def scrape(self,geolocation=True, geostring='London UK') :
		f = urllib.urlopen(self.url)
		html = f.read()
		f.close()
		soup = BeautifulSoup(html)

		# Now, let's scrap!

		self.location = self.__clean(soup('span','location')[0].contents[1])
		self.title = self.__clean(soup('div',id="title")[0].contents[0].contents[0])
		self.description = soup('div',id="desc")[0].contents[0].contents[0].contents[0]
		try:
			email1 = soup('span','email')[0].contents[2].attrs[0][1]
			if email1.startswith('/cgi-bin'):
				self.email = "http://www.gumtree.com"+email1
			else :
				self.email = email1
		except:
			self.email = ''
		try:
			self.image = "http://www.gumtree.com"+soup('div',id="images")[0].contents[1].attrs[0][1]
		except:
			self.image = ''

		#tel = clean(soup('div',id="replyto")[0].contents[0].contents[3])

		# Geocoding
		if geolocation==True:
			try:	
				search = self.location + " " + geostring
				g = geocoders.Google('ABQIAAAAu0AMQcAkvqfViJpEeSH_-hT2yXp_ZAY8_ufC3CFXhHIE1NvwkxQ0_Z6CDgX2Q08wvAh1aYjckybfeA')
				self.place, (self.lat,self.lng) = g.geocode(search)
			except:
				self.place= ''
				self.lat=''
				self.lng=''
		else:
			self.place= ''
			self.lat=''
			self.lng=''

		#print "Location: " + location
		#print "Title: " + title
		#print "Description: " + description
		#print "Email: "+email
		#print "Image: "+image

	def out(self,file) :

		# RDF output

		RDF = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
		RDFS = Namespace("http://www.w3.org/2000/01/rdf-schema#")
		GT = Namespace("http://purl.org/ontology/flat/")
		FOAF = Namespace("http://xmlns.com/foaf/0.1/")
		DC = Namespace("http://purl.org/dc/elements/1.1/")
		WGS = Namespace("http://www.w3.org/2003/01/geo/wgs84_pos#")
		graph = ConjunctiveGraph()
		
		flat = URIRef("#flat")
		p = BNode()
		e = URIRef(self.email)
		i = URIRef(self.image)
		
		graph.add((flat,RDF.type,GT['Flat']))
		graph.add((flat,FOAF['based_near'],p))
		graph.add((p,RDFS.label,Literal(self.place)))
		graph.add((p,DC['title'],Literal(self.location)))
		graph.add((p,WGS['lat'],Literal(self.lat)))
		graph.add((p,WGS['long'],Literal(self.lng)))
		graph.add((flat,FOAF['mbox'],e))
		graph.add((flat,FOAF['depiction'],i))
		graph.add((flat,DC['title'],Literal(self.title)))
		graph.add((flat,DC['description'],Literal(self.description)))

		print graph.serialize(destination=file,format='xml')




# Main
#if len(sys.argv)==3:
#	fs = FlatScrap(sys.argv[1])
#	fs.scrap()
#	fs.out(sys.argv[2])


