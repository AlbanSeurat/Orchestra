import pprint
import re
import os.path
from file import FileEx

class PutioEx(object):
	
	MOVIES_TYPE = 1
	SERIES_TYPE = 2

	def __init__(self, client):
    		self.client = client

	def parseDirectories(self, parentId, func):
		files = self.client.File.list(parentId)
		for file in files:
			if(file.content_type == "application/x-directory"):
				self.parseDirectories(file.id, func)
			else:
				func(FileEx(file))

	def getDirectory(self, name): 
		files = self.client.request("/files/search/" + name)
		if len(files["files"]):
			movieId = files["files"].pop().get("id")
			return movieId
		return None

	def getMP4Status(self, file):
		if file.content_type == "video/mp4":
			return True
		response = self.client.request("/files/" + str(file.id) + "/mp4")
		if "mp4" in response :
			if "status" in response["mp4"]:
				return response["mp4"]["status"]
		return False

	def isMP4Ready(self, file):
		response = self.getMP4Status(file)
		if type(response) is not bool:
			return response != "NOT_AVAILABLE"
		return response

	def isMP4Complete(self, file):
		response = self.getMP4Status(file)
		if type(response) is not bool:
			return response == "COMPLETED"
		return response
		
	def prepareMP4(self, file):
		self.client.request("/files/" + str(file.id) + "/mp4", method="POST")


   	def _download_file(self, file, fileName, type = ""):	
		
		cursize = os.path.getsize(fileName) if os.path.exists(fileName) else 0

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
			
		
