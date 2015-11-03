from MySQLDB import MySQLDB
from PostgreSQL import PostgreSQL

class DBFactory(object):

	def resolve(dbtype):		
		if dbtype == "MySql": return MySQLDB()
		#to be implemented
		if dbtype == "PostgreSql": return PostgreSql()

	resolve = staticmethod(resolve)
