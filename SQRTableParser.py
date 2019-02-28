#When this runs, the file given is checked for variables that are printed to the report in
#SQR -- these variables are ones that absolutely need to go into the GTT. The results are
#then plced in a file within the local directory under the name of GTTvariables.txt, sorted
#alphabetically.

#Update: Added a GUI, with a file browser.
#		 Uses Tkinter for GUI.
import Tkinter,tkFileDialog
from Tkinter import *;
import re; #regex lib

class Application(Frame):

	def createWidgets(self):    
		#Quits the app completely
		self.QUIT = Button(self)
		self.QUIT["text"] = "QUIT"
		self.QUIT["fg"]   = "red"
		self.QUIT["command"] =  self.quit
		self.QUIT.grid(row=5, column=1)
		self.QUIT.config(width="15")
		#Filepath entry field label
		self.pathLabel = Label(self, text="Filepath")
		self.pathLabel.grid(columnspan=2, row=0, column=1)
		#Varible string value for the entry field
		self.path = StringVar()
		#Entry field for the filepath
		self.pathEntry = Entry(self, width=40, takefocus=True, textvariable=self.path)
		self.pathEntry.grid(columnspan=2, row=1, column=1)
		#Browsing button for filebrowser
		self.BROWSE = Button(self)
		self.BROWSE["text"] = "BROWSE"
		self.BROWSE["fg"]   = "black"
		self.BROWSE["command"] =  self.fileBrowser
		self.BROWSE.grid(row=1, column=4)
		self.BROWSE.config(width="15")
		#When pressed, calls createFile() 
		self.SUBMIT = Button(self)
		self.SUBMIT["text"] = "SUBMIT"
		self.SUBMIT["fg"]   = "black"
		self.SUBMIT["command"] =  self.createFile
		self.SUBMIT.grid(row=5, column=2)
		self.SUBMIT.config(width="15")

	#Called from browse button
	def fileBrowser(self):
		from tkFileDialog import askopenfilename
		
		Tk().withdraw() ;
   		self.filename = askopenfilename();
   		self.path.set(self.filename);
   	#Parser code
	def createFile(self):
		try:
			#Reading file
			with open(self.pathEntry.get()) as f:
				lines = f.readlines();
			
			#Tables list, table names list
			tables = []
			tableNames = [];

			#procFlag is used to seperate procedure during parsing, without it
			#the text would be way to large to parse with regex
			procFlag = False;
			procLines = [];

			#Creating return file, declaring regex patterns to be used
			procNamePattern 	= '((?<=begin-procedure)([ ]+)([^\s]+))';
			procEndPattern = '(end-procedure)';
			fromPattern = '(?<=FROM)([\w\s,]+)(?=WHERE)';
			tablePattern = '(^(\s)*[\w]+)';
			tableFile 		= open("GTTTables.txt", "w+");
			

			#This is a complex loop so bear with me
			for line in lines:
				#Triggers if we are currently parsing a line within a procedure.
				if procFlag:
					procLines.append(line);
					procEndMatch = re.search(procEndPattern, line);
					#Triggers if we parsed end-procedure, we then
					#combine all of the lines of the procedure into one text
					#so that we can carry out a multiline regex search.
					#We also reset some variables.
					if procEndMatch:
						procFlag = False;
						fullProc = ''.join(procLines);
						procLines[:] = [];
						fromMatch = re.findall(fromPattern, fullProc, re.MULTILINE);
						#Triggers whenever we find the FOR statement within the procedure.
						#This pulls EVERY FOR statement from the procedure, but as it is now
						#we ignore all of them except for the first. The others are UNIONS.
						if fromMatch:
							#print(fromMatch);
							tableLines = fromMatch[0].splitlines();
							#Travel through the lines of the FOR statement and grab the individual
							#table names, store them into a table, and write them to the file.
							for tableLine in tableLines:
								tableMatch = re.search(tablePattern, tableLine);
								if tableMatch:
									tableNames.append(tableMatch.group().strip());
									tableFile.write('	' + tableMatch.group().strip() + '\n');
									print('	' + tableMatch.group().strip());
				#Triggers if we are in between parsing procedures
				else:
					procNameMatch = re.search(procNamePattern, line);
					if procNameMatch:
						tables.append(procNameMatch.group());
						tableFile.write(procNameMatch.group() + '\n');
						print(procNameMatch.group().strip());
						procFlag = True;

			print('File written successfully!');
		except IOError:
			print('IOError, no path specified!');


	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.pack()
		self.createWidgets()
		#self.createFile()

root = Tk()
app = Application(master=root)
app.mainloop()
#path = "C:\Users\\t0rmsanz\Documents\Work Docs\FirstConversion\wirtrnrg.txt";
root.destroy()