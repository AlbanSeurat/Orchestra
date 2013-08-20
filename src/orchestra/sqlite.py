import sqlite3
import pprint
from file import FileEx

class SQLiteEx(object):

	def __init__(self, dbname, pclient):
		self.conn = sqlite3.connect(dbname)
		self.conn.execute("CREATE TABLE if not exists files (id text primary key, type int, mp4size int, original_name text, moviedb_name text, downloaded int)");
		self.pclient = pclient


	def storeFileInfo(self, file, type):
		c = self.conn.cursor()
		c.execute("insert or ignore into files (id, type, original_name, mp4size) values (?, ?, ?, ?)", (file.id, type, file.name, file.mp4Size))
		c.execute("update files set type = ?, original_name = ?, mp4size = ? where id = ?" , (type, file.name, file.mp4Size, file.id))
		self.conn.commit()

	def listNonCompletedMovies(self, callback):
		c = self.conn.cursor()
		c.execute("select id, original_name from files where downloaded = 0 or downloaded is null");
		for row in c: 
			callback(self.pclient.getFile(int(row[0])))
			#res = self.client.request('/files/%i' % int(row[0]), method='GET')
			#file = _File(res['file'])
        		#callback(FileEx(file, self.client.getMP4Size(file)))

	def runTransact(self, func, query):
		c = self.conn.cursor()
		try:
			func()
			c.execute(query);
			self.conn.commit()
		except Exception, e:
			print e
			raise e
