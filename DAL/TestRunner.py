import DBFactory
from Results import Results
from Credentials import Credentials

if __name__ == '__main__':

	username = "cs419user"
	password = "password"
	hostname = "db4free.net"
	dbname = "cs419mysqldb"
	dbtype = "MySql"
	# query = "SELECT COLUMN_NAME FROM INFORMATION_SCHEMA'.'COLUMNS' WHERE 'TABLE_SCHEMA'= 'cs419mysqldb' AND 'TABLE_NAME' = 'users'"
	query = "INSERT INTO users(id, email,password,firstName, lastName) VALUES(null, 'test@test.com','Encrypted Password','John','Doe')"
	query = "SELECT * FROM users"
	userCreds = Credentials(username, password, hostname, dbname)
	
	dbFactory = DBFactory.DBFactory()
	database = dbFactory.resolve(dbtype)
	if database.connect(userCreds): 
		result = database.query(userCreds, query)
		num = result.getnumrows() - 1
		print "========================="
		while num > 0:
			print result.getrow(num)
			num -= 1

	query1 = "INSERT INTO users(id, email,password,firstName, lastName) VALUES(null, 'test34@test.com','Encrypted Password','Karen','Moss')"
	database.query(userCreds, query1)

	if database.connect(userCreds): 
		result = database.query(userCreds, query)
		num = result.getnumrows() - 1
		print "========================="
		while num > 0:
			print result.getrow(num)
			num -= 1

