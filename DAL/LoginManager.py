import curses
import curses.panel
import time
import sys
import DBFactory
from Credentials import Credentials
import QueryService

class LoginManager(object):

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
		port = 0
		username = ""
		password = ""
		dbtype = ""
		dbname = ""
		hostname = ""
		erase = " " * (dims[1]-2)
		while selection < 0:
			self.printMenu(self.screen, dims, option)
			action = self.screen.getch()
			if action == curses.KEY_UP:
				option = (option - 1) % 8
			elif action == curses.KEY_DOWN:
				option = (option + 1) % 8
			elif action == ord('\n'):
				selection = option
			elif action == ord('q'):
				self.screen.clear()
				curses.echo(1)
				curses.endwin()
				return			

			display = 1
			if selection == 0:
				username = self.getInput(selection-3, display, self.screen, dims, len(username)) 
				selection = -1
				option += 1
				
			elif selection == 1:
				display = 0
				password = self.getpassword(selection-3, display, self.screen, dims, len(password))			
				selection = -1
				option += 1

			elif selection == 2:
				dbtype = self.getLanguage(selection-3, self.screen, dims)
				selection = -1
				option += 1

			elif selection == 3:
				dbname = self.getInput(selection-3, display, self.screen, dims, len(dbname))
				selection = -1	
				option += 1

			elif selection == 4:
				hostname = self.getInput(selection-3, display, self.screen, dims, len(hostname))
				selection = -1	
				option += 1

			elif selection == 5:
				port = self.getInput(selection-3, display, self.screen, dims, len(str(port)))		
				try:
					int(port)
				except:
					port = 3307
				selection = -1	
				option += 1			
			elif selection == 6:
			#	self.credentials = Credentials("cs", "password", "db4free.net", "cs419mysqldb") 
				self.credentials = Credentials(username,password,hostname, int(port),dbname,dbtype) 				
				#self.credentials = Credentials("kzwjzqlulxolgt", "2oPmzkAWGOIwc9GlauZa26jeBW", "ec2-54-204-40-209.compute-1.amazonaws.com", "5432", "d38ker1opds5h3", "PostgreSQL") 
				if self.checkInput(self.credentials, dbtype) != 0:
					dbFactory = DBFactory.DBFactory()
					database = dbFactory.resolve(dbtype)					
					if database.connect(self.credentials):					
						self.database = database	
						self.screen.clear()					
						selection = -1
						return True
					else:
						self.screen.addstr((dims[0]//2)+5, 1, erase)
						self.screen.addstr((dims[0]//2)+5, (dims[1]//3)-10, "***Error: DB connection failed.***", curses.A_BOLD)		
						selection = -1
						continue	
				else:
					self.screen.addstr((dims[0]//2)+5, 1, erase)
					self.screen.addstr((dims[0]//2)+5, (dims[1]//3)-10, "***Error: Please enter a value in every field.***", curses.A_BOLD)
					selection = -1
					continue
			elif selection == 7:
				return False										
				
	def getcredentials(self):
		return self.credentials

	def getdatabase(self):
		return self.database

	def getscreen(self):
		return self.screen

	def checkInput(self, credentials, dbtype):
		if credentials.username == "" or credentials.password == "" or dbtype == "" or credentials.dbname == "" or credentials.host == "":
			return 0

	def getpassword(self, selection, viewchr, screen, dims, eraselen):
		erase = ' ' * eraselen
		self.screen.move(dims[0]/2+selection, dims[1]/3+10)
		curses.curs_set(1)
		curses.echo(viewchr)
		curses.nocbreak()
		
	        self.screen.addstr((dims[0]/2)+selection, (dims[1]/3)+10, erase)	
		self.screen.move(dims[0]/2+selection, dims[1]/3+10)        
	        newInput = screen.getstr()	
	        hidepass = '*' * len(newInput) 
		self.screen.addstr((dims[0]/2)-2, (dims[1]/3)+10, hidepass)
		
		curses.curs_set(0)
		curses.cbreak()
		curses.echo(0)
		return newInput
					
	def getInput(self, selection, viewchr, screen, dims, eraselen):	
		erase = ' ' * eraselen
		self.screen.addstr((dims[0]/2)+selection, (dims[1]/3)+10, erase)
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
		graphics = [0]*8
		graphics[option] = curses.A_REVERSE
		self.screen.addstr((dims[0]/2)-3, dims[1]/3, 'Username', graphics[0])
		self.screen.addstr((dims[0]/2)-2, dims[1]/3, 'Password', graphics[1])
		self.screen.addstr((dims[0]/2)-1, dims[1]/3, 'Database', graphics[2])
		self.screen.addstr((dims[0]/2), dims[1]/3, 'DB Name', graphics[3])
		self.screen.addstr((dims[0]/2)+1, dims[1]/3, 'Hostname', graphics[4])
		self.screen.addstr((dims[0]/2)+2, dims[1]/3, 'Port', graphics[5])
		self.screen.addstr((dims[0]/2)+3, dims[1]/3, 'Login', graphics[6])
		self.screen.addstr((dims[0]/2)+4, dims[1]/3, 'Exit', graphics[7])	
		self.screen.refresh()
