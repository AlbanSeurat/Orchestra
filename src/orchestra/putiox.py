import pprint
import re
import os.path
import logging
from file import FileEx
from putio import _File

logger = logging.getLogger(__name__)

class PutioEx(object):
	
	def __init__(self, client):
    		self.client = client
		self.vidrgx = re.compile("^video/.*$")
		self.vidnamergx = re.compile(".*sample.*", re.IGNORECASE)

	def parseDirectories(self, parentId, func):
		files = self.client.File.list(parentId)
		for file in files:
			if(file.content_type == "application/x-directory"):
				self.parseDirectories(file.id, func)
			else:
				func(FileEx(file, self.getMP4Size(file)))

	def getDirectory(self, name): 
		files = self.client.request("/files/search/" + name)
		if len(files["files"]):
			movieId = files["files"].pop().get("id")
			return movieId
		return None

	def fileExists(self, id):
		try:
			res = self.client.request('/files/%i' % id, method='GET')
			return True
		except Exception as e:
			return False

	def getFile(self, id):
		res = self.client.request('/files/%i' % id, method='GET')
		file = _File(res['file'])
		return FileEx(file, self.getMP4Size(file))

	def getMP4Infos(self, file):
		if self.vidrgx.match(file.content_type) is not None and self.vidnamergx.match(file.name) is None:
			if file.content_type == "video/mp4":
				return { u"status" : "COMPLETED", u"size" : file.size }
			response = self.client.request("/files/" + str(file.id) + "/mp4")
			if "mp4" in response :
				if "status" in response["mp4"]:
					return response["mp4"]
		return None

	def getMP4Size(self, file):
		response = self.getMP4Infos(file)
		if response is not None and "size" in response:
			return response["size"]
		return None

	def isMP4Ready(self, file):
		response = self.getMP4Infos(file)
		if response is not None:
			return response["status"] != "NOT_AVAILABLE"
		return response

	def isMP4Complete(self, file):
		response = self.getMP4Infos(file)
		if response is not None:
			return response["status"] == "COMPLETED"
		return response
		
	# returns true if mp4 is ready, false if it's not ready and none if the file is not valid
	def prepareMp4(self, file):
		if self.isMP4Ready(file) is False:
			self.client.request("/files/" + str(file.id) + "/mp4", method="POST")
		return self.isMP4Ready(file) 

   	def _download_file(self, file, fileName, type = ""):	
		
		cursize = os.path.getsize(fileName) if os.path.exists(fileName) else 0

		if(cursize < file.mp4Size):
			response = self.client.request(
        	    		'/files/%s%s/download' % (file.id, type), headers={"Range" : "bytes=%d-" % cursize }, raw=True, stream=True )
        
        		with open(fileName, 'ab') as f:
       		    		for chunk in response.iter_content(chunk_size=1024):
                			if chunk: # filter out keep-alive new chunks
                	    			f.write(chunk)
                	    			f.flush()


	def downloadMP4(self, file, fileName):
		if file.content_type == "video/mp4":
			self._download_file(file, fileName)
		else:
			self._download_file(file, fileName, "/mp4")
			
		
