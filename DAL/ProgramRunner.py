import DBFactory
from Results import Results
from Credentials import Credentials
from LoginManager import LoginManager
from QueryService import QueryService
import curses
import curses.panel
import os
import sys

if __name__ == '__main__':
	
	os.environ['LINES'] = "50"
	os.environ['COLUMNS'] = "150"
	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=50,cols=150))

	loginManager = LoginManager()
	if (loginManager.userlogin()): 
		credentials = loginManager.getcredentials()
		database = loginManager.getdatabase()
		screen = loginManager.getscreen()		
		queryService = QueryService()
		queryService.querySession(screen, credentials, database)
	os.system('reset')
	