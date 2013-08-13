import subliminal
import os.path
import pprint
import struct
import StringIO
from subliminal.services import ServiceConfig
from subliminal.services.opensubtitles import OpenSubtitles
from subliminal.videos import Video
	

class SubtitleEx:

	def __init__(self, client):
    		self.client = client
		self.fileDir = os.path.dirname(os.path.realpath(__file__))
		self.llFormat = 'q'
                self.byteSize = struct.calcsize(self.llFormat) 

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

	def downloadSubtitles(self, file, filename):
			
		video = Video.from_path(filename)
		(video.size, video.hashes["OpenSubtitles"]) = self.calculateFileSizeAndHash(file)
		
		openSubtitle = OpenSubtitles(ServiceConfig(False, os.path.join(self.fileDir, ".cache")))
		openSubtitle.init()
		subtitles = openSubtitle.list(video, subliminal.language.language_set(["EN"]))
		if(subtitles is not None):
			subtitles.sort(key=lambda s: subliminal.core.key_subtitles(s, video, ["EN"], None, [subliminal.core.MATCHING_CONFIDENCE]), reverse=True)
			openSubtitle.download(subtitles[0])
		
