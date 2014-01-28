import putio
import os.path
from putiox import PutioEx
from file import FileEx
from subtitles import SubtitleEx
from sqlite import SQLiteEx
import logging
from utils import mkdir_p

logger = logging.getLogger(__name__)

class Orchestra(object):

	def __init__(self, apiToken, moviesDir, seriesDir):
		handle = putio.Client(apiToken)
		self.pclient = PutioEx(handle)
		self.psubtitles = SubtitleEx(handle)
		self.db = SQLiteEx('orchestra.db', self.pclient)
		self.moviesDir = moviesDir
		self.seriesDir = seriesDir

		if not os.path.exists(self.moviesDir):
			os.mkdir(self.moviesDir)
		self.movieId = self.pclient.getDirectory("Movies")
		
		if not os.path.exists(self.seriesDir):
			os.mkdir(self.seriesDir)
		self.seriesId = self.pclient.getDirectory("Series")

	
	def startup(self):
		self.pclient.parseDirectories(self.movieId, self.listMovie)
		self.pclient.parseDirectories(self.seriesId, self.listSeries)
		self.db.listNonCompletedFiles(self.downloadMovieData, FileEx.MOVIES)
		self.db.listNonCompletedFiles(self.downloadSeriesData, FileEx.SERIES)


	def listMovie(self, file):
		if self.pclient.prepareMp4(file):
			self.db.storeFileInfo(file, FileEx.MOVIES)

	def listSeries(self, file):
		if self.pclient.prepareMp4(file):
			self.db.storeFileInfo(file, FileEx.SERIES)

	def downloadMovieData(self, file):
		subtitle = self.psubtitles.getSubtitles(file)
		if subtitle is not None:
			movieName = subtitle.movieName + " (" + subtitle.movieYear + ")";
			logger.info(movieName)
			self.downloadMovie(file, movieName.replace("/", "_"), subtitle)

	def downloadSeriesData(self, file):
		subtitle = self.psubtitles.getSubtitles(file)
		if subtitle is not None:
			serieEpisode = subtitle.serieName + ".s%02de%02d" % ( subtitle.serieSeason , subtitle.serieEpisode)
			logger.info(serieEpisode)
			self.downloadSerie(file, subtitle.serieName, subtitle.serieSeason, serieEpisode.replace("/", "_"), subtitle)
				

	def downloadMovie(self, file, fileName, subtitle):
		
		def __downloadMovieMP4():
			self.psubtitles.downloadSubtitles(subtitle, os.path.join(self.moviesDir, fileName) + ".srt")
			self.pclient.downloadMP4(file, os.path.join(self.moviesDir, fileName) + ".mp4")

		if self.pclient.isMP4Complete(file):
			self.db.runTransact(__downloadMovieMP4, "update files set downloaded = 1, moviedb_name = ? where id = ? ", (fileName, file.id))
			

	def downloadSerie(self, file, serieName, serieSeason, fileName, subtitle):
		
		def __downloadSerieMP4():
			episodeDir = os.path.join(self.seriesDir, serieName, "season%d" % serieSeason)
			if not os.path.exists(episodeDir):
				mkdir_p(episodeDir)
			self.psubtitles.downloadSubtitles(subtitle, os.path.join(episodeDir, fileName) + ".srt")
			self.pclient.downloadMP4(file, os.path.join(episodeDir, fileName) + ".mp4")

		if self.pclient.isMP4Complete(file):
			self.db.runTransact(__downloadSerieMP4, "update files set downloaded = 1, moviedb_name = ? where id = ? ", (fileName, file.id))
			

