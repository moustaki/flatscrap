#!/usr/bin/python
import sys
from FlatScrap import *

fs = FlatScrap(sys.argv[1])
fs.scrap()
fs.out(sys.argv[2])

