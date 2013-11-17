import os.path
import xmlrpclib
import pprint
import StringIO
import base64
import gzip
import logging
from utils import to_unicode

logger = logging.getLogger(__name__)

class OpenSubtitlesEx():
    	server_url = 'http://api.opensubtitles.org/xml-rpc'
	def __init__(self):
		self.server = xmlrpclib.ServerProxy(self.server_url)
		result = self.server.LogIn('', '', 'eng', 'subliminal v0.6')
       		if result['status'] != '200 OK':
            		raise Exception('Login failed')
        	self.token = result['token']

	def list(self, moviehash, size):
        	results = self.server.SearchSubtitles(self.token, [{'moviehash': str(moviehash), 'moviebytesize': str(size), 'sublanguageid' : 'eng' }])
		logger.debug(results)
        	subtitles = []
		if results is not None and results['data'] is not False:
 			for result in results['data']:
				subtitles.append(Subtitle(result['SubDownloadLink'], result['SubFileName'], result['MovieName'], result['MovieYear'], result['IDSubtitleFile']))
       		return subtitles



	def download(self, subtitle, filename):

		results = self.server.DownloadSubtitles(self.token, [subtitle.subFileId])
		if results and results['data']:
			try:
				fstr = StringIO.StringIO(base64.b64decode(results['data'][0]['data']))
				with open(filename, "wb") as dump:
					with gzip.GzipFile(fileobj=fstr) as gz:
						dump.write(gz.read())
						dump.close()
						gz.close()
			except Exception as e:
		   	 	#if os.path.exists(subtitle.path):
		        	#	os.remove(subtitle.path)
		    		raise Exception(str(e))
		


class Subtitle(object):
	
	def __init__(self, downloadLink, fileName, movieName, movieYear, subFileId):
		self.downloadLink = downloadLink
		self.fileName = to_unicode(fileName)
		self.movieName = movieName
		self.movieYear = movieYear
		self.subFileId = subFileId


	def __repr__(self):
		return "%s<%s : %s - %s>" % (self.__class__.__name__, self.fileName.encode('ascii', 'ignore'), self.downloadLink, self.movieName + "(" + self.movieYear + ")" )

