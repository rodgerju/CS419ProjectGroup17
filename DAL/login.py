import curses
import curses.panel
import time
import sys
import displayQueries

def login():
	screen = curses.initscr()
	screen.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	dims = screen.getmaxyx()
	screen.nodelay(0)
	screen.clear()

	selection = -1
	option = 0
	userName = ""
	pword = ""
	dataBase = ""
	dbName = ""
	hostName = ""

	while selection < 0:
		printMenu(screen, dims, option)
		action = screen.getch()
		if action == curses.KEY_UP:
			option = (option - 1) % 6
		elif action == curses.KEY_DOWN:
			option = (option + 1) % 6
		elif action == ord('\n'):
			selection = option
		elif action == ord('q'):
			screen.clear()
			curses.echo(1)
			curses.endwin()
			return

		if selection == 0:
			userName = getInput(selection-3, 1, screen, dims) 
			selection = -1
			option += 1
			
		elif selection == 1:
			pword = getInput(selection-3, 0, screen, dims)			
			selection = -1
			option += 1

		elif selection == 2:
			dataBase = getLanguage(selection-3, screen, dims)
			selection = -1
			option += 1

		elif selection == 3:
			dbName = getInput(selection-3, 1, screen, dims)
			selection = -1	
			option += 1

		elif selection == 4:
			hostName = getInput(selection-3, 1, screen, dims)
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

def getInput(selection, pword, screen, dims):	
	screen.move(dims[0]/2+selection, dims[1]/3+10)
	curses.curs_set(1)
	curses.echo(pword)
	curses.nocbreak()
	newInput = screen.getstr()
	curses.curs_set(0)
	curses.cbreak()
	curses.echo(0)
	return newInput

def getLanguage(selection, screen, dims):	
	dataList = ["MySql", "PostgreSQL"]
	optionData = 0	
	while 1:
		screen.addstr((dims[0]/2+selection), dims[1]/3+10, (dataList[optionData]+"       "))
		action = screen.getch()
		if action == curses.KEY_UP or action == curses.KEY_DOWN:
			optionData = (optionData + 1) % 2
		elif action == ord('\n'):
			return dataList[optionData]

def printMenu(screen, dims, option):	
	graphics = [0]*6
	graphics[option] = curses.A_REVERSE
	screen.addstr((dims[0]/2)-3, dims[1]/3, 'Username', graphics[0])
	screen.addstr((dims[0]/2)-2, dims[1]/3, 'Password', graphics[1])
	screen.addstr((dims[0]/2)-1, dims[1]/3, 'Database', graphics[2])
	screen.addstr((dims[0]/2), dims[1]/3, 'DB Name', graphics[3])
	screen.addstr((dims[0]/2)+1, dims[1]/3, 'Hostname', graphics[4])
	screen.addstr((dims[0]/2)+2, dims[1]/3, 'Login', graphics[5])
	screen.refresh()

def dataView():
	screen.clear()
	

if __name__ == '__main__':
	login()
