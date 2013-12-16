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

	def _performHash(self, hash, content):

		f = StringIO.StringIO(content)
		for x in range(65536/self.byteSize): 
                        buffer = f.read(self.byteSize) 
                        (l_value,)= struct.unpack(self.llFormat, buffer)  
                        hash += l_value 
                        hash = hash & 0xFFFFFFFFFFFFFFFF 
		f.close()
		return hash

	def calculateFileSizeAndHash(self, file):

		response = self.client.request('/files/%d' % file.id )
		return (response["file"]["size"], response["file"]["opensubtitles_hash"])

		#response = self.client.request('/files/%d/download' % file.id, headers={"Range" : "bytes=0-65535" }, raw=True, stream=True )
                #hash = self._performHash(hash, response.content)

		#response = self.client.request('/files/%d/download' % file.id, headers={"Range" : "bytes=%d-" % (filesize - 65536) }, raw=True, stream=True )
                #hash = self._performHash(hash, response.content)

		#return (filesize, "%016x" % hash)

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
				if p.match(fileName):
					return sub	
		return None
	
	def downloadSubtitles(self, subtitle, fileName):
		self.openSubtitle.download(subtitle, fileName)
		
