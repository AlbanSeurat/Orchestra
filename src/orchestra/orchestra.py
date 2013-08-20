import putio
import os.path
import pprint
from putiox import PutioEx
from file import FileEx
from subtitles import SubtitleEx
from sqlite import SQLiteEx
import logging

logger = logging.getLogger(__name__)

class Orchestra(object):

	def __init__(self, apiToken, moviesDir):
		handle = putio.Client(apiToken)
		self.pclient = PutioEx(handle)
		self.psubtitles = SubtitleEx(handle)
		self.db = SQLiteEx('orchestra.db', self.pclient)
		self.moviesDir = moviesDir

		if not os.path.exists(self.moviesDir):
			os.mkdir(self.moviesDir)
		self.movieId = self.pclient.getDirectory("Movies")

	
	def startup(self):
		self.pclient.parseDirectories(self.movieId, self.listMovie)
		self.db.listNonCompletedMovies(self.prepareMovieData)


	def listMovie(self, file):
		if self.pclient.prepareMp4(file):
			self.db.storeFileInfo(file, FileEx.MOVIES)

	def prepareMovieData(self, file):
		subtitle = self.psubtitles.getSubtitles(file)
		movieName = subtitle.movieName + " (" + subtitle.movieYear + ")";
		logger.info(movieName)
		self.downloadFile(file, movieName, subtitle)
		
		
	def downloadFile(self, file, fileName, subtitle):
		if self.pclient.isMP4Complete(file):
			self.downloadMp4(file, fileName, subtitle)

	def downloadMp4(self, file, fileName, subtitle):
		
		def __downloadMP4():
			self.pclient.downloadMP4(file, os.path.join(self.moviesDir, fileName) + ".mp4")
			self.psubtitles.downloadSubtitles(subtitle, os.path.join(self.moviesDir, fileName) + ".srt")
	
		self.db.runTransact(__downloadMP4, "update files set downloaded = 1, moviedb_name = '%s' where id = '%d' " % (fileName, file.id))
			

