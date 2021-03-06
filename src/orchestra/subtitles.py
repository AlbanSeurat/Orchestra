import os.path
import pprint
import struct
import StringIO
import logging
import re
from opensubtitle import OpenSubtitlesEx

logger = logging.getLogger(__name__)

class SubtitleEx(object):

	pSub = re.compile('[\W\s]+')

	def __init__(self, client):
    		self.client = client
		self.llFormat = 'q'
                self.byteSize = struct.calcsize(self.llFormat) 
		self.openSubtitle = OpenSubtitlesEx()

	def calculateFileSizeAndHash(self, file):

		response = self.client.request('/files/%d' % file.id )
		return (response["file"]["size"], response["file"]["opensubtitles_hash"])

	def getSubtitles(self, file):
		(filesize, filehash) = self.calculateFileSizeAndHash(file)
		logger.debug("file (%s) : size : %d, hash %s" % (file.name, filesize, filehash))
		subtitles = self.openSubtitle.list(filehash, filesize)
		logger.debug("subtitles %s" % subtitles)
		if subtitles is not None:
			for sub in subtitles:
				subName = self.pSub.sub('', sub.simpleName)
				fileName = self.pSub.sub('', file.name)	
				p = re.compile(".*%s.*" % subName, re.IGNORECASE)
				logger.debug("match %s to %s" % (subName, fileName))
				if len(subName) > 0 and p.match(fileName):
					return sub	
		return None
	
	def downloadSubtitles(self, subtitle, fileName):
		self.openSubtitle.download(subtitle, fileName)
		
