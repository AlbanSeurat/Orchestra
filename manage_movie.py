#!/usr/bin/python
import logging
import sys
from orchestra import Orchestra

#logging.basicConfig(level=logging.DEBUG, format='%(levelname)-8s %(asctime)s %(name)-24s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')

main = Orchestra(sys.argv[1])

main.startup()

#files = client.request("/files/search/Series")
#if len(files["files"]):
#        seriesId = files["files"].pop().get("id")
#SupermanFiles = client.File.list(parentId);	
#pprint.pprint(client.File.list(movieId));




