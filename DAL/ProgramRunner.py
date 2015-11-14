import DBFactory
from Results import Results
from Credentials import Credentials
from login import login
from displayQueries import displayQueries
import curses
import curses.panel

if __name__ == '__main__':

	login = login()
	if (login.userlogin()): 
		credentials = login.getcredentials()
		database = login.getdatabase()
		screen = login.getscreen()		
		session = displayQueries()
		session.querySession(screen, credentials, database)

	#Need to print error message here: Failed login
	#else:
