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
			
			#Variables list
			variables = []
			#Creating return file, declaring regex patterns to be used
			printedPattern 	= '((#|\$|&)[A-Za-z0-9._%+-]+)([\s]+)(\([0-9,+ ]+\))';
			variablePattern = '((#|\$|&)[A-Za-z0-9._%+-]+)';
			variableFile = open("GTTvariables.txt", "w+");
			for line in lines:
				#This match finds the next chunk of text that matches one that is being printed to the report
				match = re.search(printedPattern, line);
				if match:
					printedLine = match.group();
					#This match simply retrieves the variable name so we can store it without the bloat
					match = re.search(variablePattern, printedLine);
					if match.group() not in variables:
						variables.append(match.group());
						print(match.group());

			#Sorting the list and printing it to the return file
			variables.sort();
			for variable in variables:
				variableFile.write(variable + '\n');
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