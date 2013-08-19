from putio import _File
import pprint

class FileEx(_File):
	
	MOVIES = 1
	SERIES = 2

	def __init__(self, other = None):
        	if other:
			self.__dict__ = dict(other.__dict__)
	
	

