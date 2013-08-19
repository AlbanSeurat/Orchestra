import sqlite3
import pprint
from file import FileEx
from putio import _File

class SQLiteEx(object):

	def __init__(self, dbname, client):
		self.conn = sqlite3.connect(dbname)
		self.conn.execute("CREATE TABLE if not exists files (id text primary key, type int, original_name text, moviedb_name text, downloaded int)");
		self.client = client


	def storeFileInfo(self, file, type):
		c = self.conn.cursor()
		c.execute("insert or ignore into files (id, type, original_name) values ('%s', %d, '%s')" % (file.id, type, file.name))
		self.conn.commit()

	def listNonCompletedMovies(self, callback):
		c = self.conn.cursor()
		c.execute("select id, original_name from files where downloaded = 0 or downloaded is null");
		for row in c: 
			res = self.client.request('/files/%i' % int(row[0]), method='GET')
        		callback(_File(res['file']))

	def runTransact(self, func, query):
		c = self.conn.cursor()
		try:
			func()
			c.execute(query);
			self.conn.commit()
		except Exception, e:
			print e
			raise e
