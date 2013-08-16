from putio import _File
import pprint
import guessit

class FileEx(_File):
	
	MOVIES = 1
	SERIES = 2

	def __init__(self, other = None):
        	if other:
			self.__dict__ = dict(other.__dict__)
		self.guess = guessit.guess_movie_info(self.name)
	
	

