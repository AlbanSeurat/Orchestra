import pprint
import re
import os.path

class PutioEx:
	def __init__(self, client):
    		self.client = client

	def parseDirectories(self, parentId, func):
		files = self.client.File.list(parentId)
		for file in files:
			if(file.content_type == "application/x-directory"):
				self.parseDirectories(file.id, func)
			else:
				func(file)

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


   	def _download_file(self, file, storeFunc, getName, dest, type = ""):	
		
		filename = os.path.join(dest, getName()) if getName() is not None else None
		cursize = os.path.getsize(filename) if filename is not None and os.path.exists(filename) else 0
		
        	response = self.client.request(
        	    '/files/%s%s/download' % (file.id, type), headers={"Range" : "bytes=%d-" % cursize }, raw=True, stream=True )
        
       		filename = re.match(
            		'attachment; filename=(.*)',
            		response.headers['content-disposition']).groups()[0]
        
		# If file name has spaces, it must have quotes around.
	        filename = filename.strip('"')

		#store the function into the database in case and error occured during the download
		storeFunc(filename)

        	with open(os.path.join(dest, filename), 'ab') as f:
       		     for chunk in response.iter_content(chunk_size=1024):
                	if chunk: # filter out keep-alive new chunks
                	    f.write(chunk)
                	    f.flush()


	def downloadMP4(self, file, storeFunc, getName, dest):
		if file.content_type == "video/mp4":
			self._download_file(file, storeFunc, getName, dest)
		else:
			self._download_file(file, storeFunc, getName, dest, "/mp4")
			
		
