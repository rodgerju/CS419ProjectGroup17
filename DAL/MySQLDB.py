from AbstractDatabase import AbstractDatabase
from Results import Results
import Credentials
import MySQLdb
import MySQLdb.cursors as cursors
import re

class MySQLDB(AbstractDatabase):

	def connect(self, Credentials):		
		try:
			db = MySQLdb.connect(host=Credentials.host, 
			port = 3307,
			user = Credentials.username, 
			passwd= Credentials.password, 
			db = Credentials.dbname, cursorclass=cursors.SSCursor)
			db.close()
			return True
		except:
			return False		

	def query(self, credentials, query):
		try:
			conn = MySQLdb.connect(host=credentials.host, 
			port = 3307,
			user = credentials.username, 
			passwd= credentials.password, 
			db = credentials.dbname, cursorclass=cursors.SSCursor)
			cursor = conn.cursor()
			cursor.execute(query)
			
			command = self.parsecommand(query)
			result = Results()
			if (command != "select"):
				self.commitchanges(conn)			
			else:
				self.extractdata(result, cursor)			
			cursor.close()
			return result	
		except Exception as ex:
			raise ex

	def extractdata(self, result, cursor):
		result.setnumrows(len(cursor.description))
		result.setcolumns([i[0] for i in cursor.description])
		for row in cursor:
				result.addrow(row)

	def commitchanges(self, conn):
		try:
			conn.commit()				
		except Exception as ex:
			conn.rollback()
			raise ex
			
	def parsecommand(self, query):		
			return (query.split(' ', 1)[0]).lower()