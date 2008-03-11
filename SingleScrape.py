#!/usr/bin/python
import sys
from FlatScrape import *

fs = FlatScrape(sys.argv[1])
fs.scrape()
fs.out(sys.argv[2])

