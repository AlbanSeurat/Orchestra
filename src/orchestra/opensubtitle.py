import os.path
import xmlrpclib
import pprint
import StringIO
import base64
import gzip
import logging
import re
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
				if result['MovieKind'] == "episode":
					subtitles.append(SerieSubtitle(result['SubDownloadLink'], result['SubFileName'], result['IDSubtitleFile'], result['MovieName'], result['SeriesSeason'], result['SeriesEpisode']))
				else:		
					subtitles.append(MovieSubtitle(result['SubDownloadLink'], result['SubFileName'], result['IDSubtitleFile'], result['MovieName'], result['MovieYear']))
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
	
	def __init__(self, downloadLink, fileName, subFileId, simpleName):
		self.downloadLink = downloadLink
		self.fileName = to_unicode(fileName)
		self.subFileId = subFileId
		self.simpleName = simpleName

class MovieSubtitle(Subtitle):
	
	def __init__(self, downloadLink, fileName, subFileId, movieName, movieYear):
		super(MovieSubtitle, self).__init__(downloadLink, fileName, subFileId, movieName)
		self.movieName = movieName
		self.movieYear = movieYear


	def __repr__(self):
		return "%s<%s : %s - %s>" % (self.__class__.__name__, self.fileName.encode('ascii', 'ignore'), self.downloadLink, self.movieName + "(" + self.movieYear + ")" )



class SerieSubtitle(Subtitle):
	p = re.compile("\"([^\"]*)\" (.*)")
	
	def __init__(self, downloadLink, fileName, subFileId, serieName, serieSeason, serieEpisode):
		super(SerieSubtitle, self).__init__(downloadLink, fileName, subFileId, serieName)
		m = self.p.match(serieName)
		self.serieName = m.group(1)
		self.episodeName = m.group(2)
		self.simpleName = self.serieName
		self.serieSeason = int(serieSeason)
		self.serieEpisode = int(serieEpisode)


	def __repr__(self):
		return "%s<%s : %s - %s>" % (self.__class__.__name__, self.fileName.encode('ascii', 'ignore'), self.downloadLink, self.serieName + ".s%02de%02d" % ( self.serieSeason , self.serieEpisode) + " " + self.episodeName )


