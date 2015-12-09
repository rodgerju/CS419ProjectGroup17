import DBFactory
from Results import Results
from Credentials import Credentials
from login import login
from displayQueries import displayQueries
import curses
import curses.panel
import os
import sys

if __name__ == '__main__':
	
	os.environ['LINES'] = "50"
	os.environ['COLUMNS'] = "150"
	sys.stdout.write("\x1b[8;{rows};{cols}t".format(rows=50,cols=150))

	login = login()
	if (login.userlogin()): 
		credentials = login.getcredentials()
		database = login.getdatabase()
		screen = login.getscreen()		
		session = displayQueries()
		session.querySession(screen, credentials, database)
	os.system('reset')
	#Need to print error message here: Failed login
	#else:
