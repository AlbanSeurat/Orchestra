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

	def listNonCompletedFiles(self, callback, fileType):
		c = self.conn.cursor()
		c.execute("select id, original_name from files where downloaded = 0 or downloaded is null and type = %d" % fileType);
		for row in c:
			if self.pclient.fileExists(int(row[0])):
				callback(self.pclient.getFile(int(row[0])))
			else:
				c.execute("delete from files where id = %d" % int(row[0]));
				self.conn.commit()

	def runTransact(self, func, query, queryParam):
		c = self.conn.cursor()
		try:
			func()
			c.execute(query, queryParam);
			self.conn.commit()
		except Exception, e:
			print e
			raise e
