#!/usr/bin/python
import putio
import pprint
import sys
import dateutil.parser
from orchestra import Orchestra

main = Orchestra(sys.argv[1])

main.startup()

#files = client.request("/files/search/Series")
#if len(files["files"]):
#        seriesId = files["files"].pop().get("id")
#SupermanFiles = client.File.list(parentId);	
#pprint.pprint(client.File.list(movieId));




