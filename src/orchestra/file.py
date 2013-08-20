from putio import _File
import pprint

class FileEx(_File):
	
	MOVIES = 1
	SERIES = 2

	def __init__(self, other = None, mp4Size = None):
        	if other:
			self.__dict__ = dict(other.__dict__)
		self.mp4Size = mp4Size
	
	

