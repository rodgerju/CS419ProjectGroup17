from MySQLDB import MySQLDB
from PostgreSQL import PostgreSQL

class DBFactory(object):

	def resolve(dbtype):		
		if dbtype == "MySql": return MySQLDB()
		if dbtype == "PostgreSQL": return PostgreSQL()
	resolve = staticmethod(resolve)
