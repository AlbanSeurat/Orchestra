import sqlite3
import putio
import os.path
import pprint
import re
from putiox import PutioEx

class Orchestra:
	MOVIES_DIR = "movies"

	def __init__(self, apiToken):
		self.conn = sqlite3.connect('orchestra.db')
		self.pclient = PutioEx(putio.Client(apiToken))

		if not os.path.exists(Orchestra.MOVIES_DIR):
			os.mkdir(Orchestra.MOVIES_DIR)
		self.movieId = self.pclient.getDirectory("Movies")

		self.vidrgx = re.compile("^video/.*$")
		self.vidnamergx = re.compile(".*sample.*", re.IGNORECASE)
	
	def startup(self):
		
		self.pclient.parseDirectories(self.movieId, self.downloadFile)

	def downloadFile(self, file):
		if self.prepareMp4(file):
			self.downloadMp4(file)

	def downloadMp4(self, file):
		c = self.conn.cursor()
		
		def storeMP4Name(filename):
			c.execute("insert or replace into movies (id, name, path, completed) values (%d, '%s', '%s', 0) " % ( file.id, filename, Orchestra.MOVIES_DIR + "/" + filename))
			self.conn.commit()

		def getMP4Name():
			c.execute("select name from movies where id = " + str(file.id) );
			row = c.fetchone()
			return row[0] if row is not None else None

		c.execute("select exists(select 1 from movies where id = " + str(file.id) + " and completed = 1 limit 1)");
		if c.fetchone()[0] == 0:
			try:
				self.pclient.downloadMP4(file, storeMP4Name, getMP4Name, Orchestra.MOVIES_DIR)
				c.execute("update movies set completed = 1 where id = %d " % file.id)
				self.conn.commit()
			except Exception, e:
				print e
		

	def prepareMp4(self, file):
		if self.vidrgx.match(file.content_type) is not None and self.vidnamergx.match(file.name) is None:
			if not self.pclient.isMP4Ready(file):
				self.pclient.prepareMP4(file)
			return self.pclient.isMP4Complete(file)
		return False
			

