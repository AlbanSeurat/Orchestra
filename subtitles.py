import os.path
import pprint
import struct
import StringIO
from opensubtitle import OpenSubtitlesEx
	

class SubtitleEx(object):

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
		hash = filesize = response["file"]["size"]

		response = self.client.request('/files/%d/download' % file.id, headers={"Range" : "bytes=0-65535" }, raw=True, stream=True )
                hash = self._performHash(hash, response.content)

		response = self.client.request('/files/%d/download' % file.id, headers={"Range" : "bytes=%d-" % (filesize - 65536) }, raw=True, stream=True )
                hash = self._performHash(hash, response.content)

		return (filesize, "%016x" % hash)

	def getSubtitles(self, file):
		(filesize, filehash) = self.calculateFileSizeAndHash(file)
		subtitles = self.openSubtitle.list(filehash, filesize)
		if subtitles:	
			return subtitles[0]
		else:
			return None
	
	def downloadSubtitles(self, subtitle, fileName):
		self.openSubtitle.download(subtitle, fileName)
		
