import putio
import os.path
import pprint
import re
from putiox import PutioEx
from file import FileEx
from subtitles import SubtitleEx
from sqlite import SQLiteEx

class Orchestra(object):

	def __init__(self, apiToken, moviesDir):
		handle = putio.Client(apiToken)
		self.pclient = PutioEx(handle)
		self.psubtitles = SubtitleEx(handle)
		self.db = SQLiteEx('orchestra.db', handle)
		self.moviesDir = moviesDir

		if not os.path.exists(self.moviesDir):
			os.mkdir(self.moviesDir)
		self.movieId = self.pclient.getDirectory("Movies")

		self.vidrgx = re.compile("^video/.*$")
		self.vidnamergx = re.compile(".*sample.*", re.IGNORECASE)
	
	def startup(self):
		self.pclient.parseDirectories(self.movieId, self.listMovie)
		self.db.listNonCompletedMovies(self.prepareMovieData)

	def listMovie(self, file):
		if self.prepareMp4(file):
			self.db.storeFileInfo(file, FileEx.MOVIES)

	def downloadFile(self, file, fileName):
		if self.pclient.isMP4Complete(file):
			self.downloadMp4(file, fileName)

	def downloadMp4(self, file, fileName):
		
		def __downloadMP4():
			self.pclient.downloadMP4(file, os.path.join(self.moviesDir, fileName) + ".mp4")
	
		self.db.runTransact(__downloadMP4, "update files set downloaded = 1, moviedb_name = '%s' where id = '%d' " % (fileName, file.id))
		
	
	def prepareMovieData(self, file):
		subtitle = self.psubtitles.getSubtitles(file)
		movieName = subtitle.movieName + " (" + subtitle.movieYear + ")";
		pprint.pprint(movieName)
		self.downloadFile(file, movieName)
		self.psubtitles.downloadSubtitles(subtitle, os.path.join(self.moviesDir, movieName) + ".srt")

	def prepareMp4(self, file):
		if self.vidrgx.match(file.content_type) is not None and self.vidnamergx.match(file.name) is None:
			if not self.pclient.isMP4Ready(file):
				self.pclient.prepareMP4(file)
			return self.pclient.isMP4Ready(file)
		return False
			

