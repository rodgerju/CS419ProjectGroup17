import curses
import curses.panel
import time
import sys
import DBFactory
from Credentials import Credentials
import displayQueries

class login(object):

	def __init__(self):
		self.credentials = 0
		self.database = 0
		self.screen = 0

	def userlogin(self):
		self.screen = curses.initscr()
		self.screen.keypad(1)
		curses.noecho()
		curses.curs_set(0)
		dims = self.screen.getmaxyx()
		self.screen.nodelay(0)
		self.screen.clear()
		self.screen.border(0)

		selection = -1
		option = 0
		username = ""
		password = ""
		dbtype = ""
		dbname = ""
		hostname = ""

		while selection < 0:
			self.printMenu(self.screen, dims, option)
			action = self.screen.getch()
			if action == curses.KEY_UP:
				option = (option - 1) % 6
			elif action == curses.KEY_DOWN:
				option = (option + 1) % 6
			elif action == ord('\n'):
				selection = option
			elif action == ord('q'):
				self.screen.clear()
				curses.echo(1)
				curses.endwin()
				return
			
<<<<<<< HEAD
		elif selection == 1:
			display = 0
			pword = getpassword(selection-3, display, screen, dims)			
			selection = -1
			option += 1

		elif selection == 2:
			dataBase = getLanguage(selection-3, screen, dims)
			selection = -1
			option += 1

		elif selection == 3:
			dbName = getInput(selection-3, display, screen, dims)
			selection = -1	
			option += 1

		elif selection == 4:
			hostName = getInput(selection-3, display, screen, dims)
			selection = -1	
			option += 1
		
		elif selection == 5:
			if checkInput(userName, pword, dataBase, dbName, hostName) != 0:
				displayQueries.connectDatabase(screen, userName, pword, dataBase, hostName, dbName)				
				screen.clear()
			selection = -1

def checkInput(userName, pword, dataBase, dbName, hostName):
	if userName == "" or pword == "" or dataBase == "" or dbName == "" or hostName == "":
		return 0

def getpassword(selection, viewchr, screen, dims):
	erase = ' ' * 50
	screen.move(dims[0]/2+selection, dims[1]/3+10)
	curses.curs_set(1)
	curses.echo(viewchr)
	curses.nocbreak()
	
        screen.addstr((dims[0]/2)-2, (dims[1]/3)+10, erase)	
	screen.move(dims[0]/2+selection, dims[1]/3+10)        
        newInput = screen.getstr()	
        hidepass = '*' * len(newInput) 
	screen.addstr((dims[0]/2)-2, (dims[1]/3)+10, hidepass)
	
	curses.curs_set(0)
	curses.cbreak()
	curses.echo(0)
	return newInput
=======
			display = 1
			if selection == 0:
				username = self.getInput(selection-3, display, self.screen, dims) 
				selection = -1
				option += 1
				
			elif selection == 1:
				display = 0
				password = self.getpassword(selection-3, display, self.screen, dims)			
				selection = -1
				option += 1

			elif selection == 2:
				dbtype = self.getLanguage(selection-3, self.screen, dims)
				selection = -1
				option += 1

			elif selection == 3:
				dbname = self.getInput(selection-3, display, self.screen, dims)
				selection = -1	
				option += 1

			elif selection == 4:
				hostname = self.getInput(selection-3, display, self.screen, dims)
				selection = -1	
				option += 1
			
			elif selection == 5:
				self.credentials = Credentials("cs419user", "password", "db4free.net", "cs419mysqldb")
				if self.checkInput(self.credentials, dbtype) != 0:
					dbFactory = DBFactory.DBFactory()
					database = dbFactory.resolve(dbtype)					
					if database.connect(self.credentials):					
						self.database = database	
						self.screen.clear()					
						selection = -1
						return True
					else:
					#	TODO: NEED TO IMPLEMENT ERROR HANDLING FOR FAILED LOGIN
						selection = -1
						return False
														
>>>>>>> f12c161df4052905e7de4b485ed6a7d3a6ba9eae
				
	def getcredentials(self):
		return self.credentials

	def getdatabase(self):
		return self.database

	def getscreen(self):
		return self.screen

	def checkInput(self, credentials, dbtype):
		if credentials.username == "" or credentials.password == "" or dbtype == "" or credentials.dbname == "" or credentials.host == "":
			return 0

	def getpassword(self, selection, viewchr, screen, dims):
		erase = ' ' * 50
		self.screen.move(dims[0]/2+selection, dims[1]/3+10)
		curses.curs_set(1)
		#curses.echo(viewchr)
		curses.nocbreak()
		
	        self.screen.addstr((dims[0]/2)-2, (dims[1]/3)+10, erase)	
		self.screen.move(dims[0]/2+selection, dims[1]/3+10)        
	        newInput = screen.getstr()	
	        hidepass = '*' * len(newInput) 
		self.screen.addstr((dims[0]/2)-2, (dims[1]/3)+10, hidepass)
		
		curses.curs_set(0)
		curses.cbreak()
		curses.echo(0)
		return newInput
					
	def getInput(self, selection, viewchr, screen, dims):	
		self.screen.move(dims[0]/2+selection, dims[1]/3+10)
		curses.curs_set(1)
		curses.echo(viewchr)
		curses.nocbreak()
		newInput = screen.getstr()
		curses.curs_set(0)
		curses.cbreak()
		curses.echo(0)
		return newInput

	def getLanguage(self, selection, screen, dims):	
		dataList = ["MySql", "PostgreSQL"]
		optionData = 0	
		while 1:
			self.screen.addstr((dims[0]/2+selection), dims[1]/3+10, (dataList[optionData]+"       "))
			action = screen.getch()
			if action == curses.KEY_UP or action == curses.KEY_DOWN:
				optionData = (optionData + 1) % 2
			elif action == ord('\n'):
				return dataList[optionData]

	def printMenu(self, screen, dims, option):	
		graphics = [0]*6
		graphics[option] = curses.A_REVERSE
		self.screen.addstr((dims[0]/2)-3, dims[1]/3, 'Username', graphics[0])
		self.screen.addstr((dims[0]/2)-2, dims[1]/3, 'Password', graphics[1])
		self.screen.addstr((dims[0]/2)-1, dims[1]/3, 'Database', graphics[2])
		self.screen.addstr((dims[0]/2), dims[1]/3, 'DB Name', graphics[3])
		self.screen.addstr((dims[0]/2)+1, dims[1]/3, 'Hostname', graphics[4])
		self.screen.addstr((dims[0]/2)+2, dims[1]/3, 'Login', graphics[5])
		self.screen.refresh()

	def dataView():
		#why is this function here?
		self.screen.clear()
		

