from Tkinter import *
import tkFileDialog             #allows for file open, save
import tkMessageBox as mbox     #tkMessageBox is a message box (mbox) from tkinter (warning, question, error, info)
import subprocess               #Trying to use subprocess.call(cmd) to pass a print (lp or lpr) command to print document...harder than it sounds apparently
import tkColorChooser           #importing this for choosing background of text widget (self.txt)



#global variable for title of program
typer_title = "Typer 0.0.1 Pre-Alpha"

#opening the Typer configuration file
typerconf = open('typer.conf', 'r+')
conflist = open('typer.conf').readlines()

#creating the class
class TyperClass(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        self.parent = parent
        self.TyperSetup()

        #since Typer opens up with no file being opened, file_opened can be False by default
        self.file_opened = False


    def TyperSetup(self):
        #using file_opened to determine if a file is currently open
        self.file_opened = False

        #since Typer opens up with no file being opened, current_file can be the empty string by default
        self.current_file = ""

        #Typer opens in windowed mode by defauly, so therefore is_fullscreen is False
        self.is_fullscreen = False

        #setting the title of the parent (the frame itself in this case) as typer_title which is defined above...also packing happening
        self.parent.title(typer_title)
        self.pack(fill=BOTH, expand=1)

        #setting a variable to hold the background color from the typer.conf file. It is on the first line of typer.conf
        #we then set self.background to back after stripping the new line off the end of it
        back = typerconf.readline()
        back = back.rstrip('\n')
        self.background = back


        #we now start setting up the gui by creating a bunch of the menus. We then add each section as a cascade to the menubar
        #each menu added as cascade has a command on it, and most have an accelerator (keyboard shortcut)
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        #this is the File menu, holds open, save as, save, print, and file commands
        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen, accelerator="Command+o")
        fileMenu.add_command(label="Save As", command=self.onSaveAs, accelerator="Command+Shift+S")
        fileMenu.add_command(label="Save", command=self.onSave, accelerator="Command+S")
        fileMenu.add_command(label="Print", command=self.onPrint, accelerator="Command+P")
        menubar.add_cascade(label="File", menu=fileMenu)

        #this is the system menu, holds quit, copy path of file, and toggle fullscreen,
        system = Menu(menubar)
        system.add_command(label="Quit", command=self.onQuit, accelerator="Command+w")
        system.add_command(label="Copy Path of File", command=self.onCopyPath, accelerator="Command+Shift+p")
        system.add_command(label="Toggle Fullscreen", command=self.onToggleFullScreen, accelerator="Command+Shift+f")
        menubar.add_cascade(label="System", menu=system)

        #this is the edit menu, holds select all, cut, copy, and paste
        edit = Menu(menubar)
        edit.add_command(label="Select All", command=self.onSelectAll, accelerator="Command+a")
        edit.add_command(label="Cut", command=self.onCut, accelerator="Command+x")
        edit.add_command(label="Copy", command=self.onCopy, accelerator="Command+c")
        edit.add_command(label="Paste", command=self.onPaste, accelerator="Command+v")
        menubar.add_cascade(label="Edit", menu=edit)

        #this is the info menu, holds show info, whats new, open source code, and license
        infoMenu = Menu(menubar)
        infoMenu.add_command(label="Show Info", command=self.onShowInfo, accelerator="Command+Option+I")
        infoMenu.add_command(label="What's new?", command=self.onWhatsNew, accelerator="Command+Option+N")
        infoMenu.add_command(label="Open Source Code", command=self.onOpenSourceCode)
        infoMenu.add_command(label="License", command=self.onLicense)
        menubar.add_cascade(label="Info", menu=infoMenu)

        #this is the personalize menu, holds background...will hold other defaults that user can choose in future
        personalize = Menu(menubar)
        personalize.add_command(label="Background", command=self.onBackground, accelerator="Command+Shift+B")
        menubar.add_cascade(label="Personalize", menu=personalize)

        #this is the run menu, holds options to run python and java files. Will add more options in the future
        run = Menu(menubar)
        run.add_command(label="Run Python File", command=self.runPython, accelerator="Command+Option+P")
        run.add_command(label="Run Java File", command=self.runJava, accelerator="Command+Option+J")
        menubar.add_cascade(label="Run", menu=run)

        #this is the document menu, holds font, font size, and font color choices. Not yet implemented fully
        doc = Menu(menubar)
        doc.add_command(label="Font", command=self.onFont)
        doc.add_command(label="Font Size", command=self.onFontSize)
        doc.add_command(label="Font Color", command=self.onFontColor)
        menubar.add_cascade(label="Document", menu=doc)

        #here we set up the right click options so you can right click to cut, copy, and paste
        self.menu = Menu(self.parent, tearoff=0)
        self.menu.add_command(label="Cut", command=self.onCut)
        self.menu.add_command(label="Copy", command=self.onCopy)
        self.menu.add_command(label="Paste", command=self.onPaste)

        #here we bind the keyboard shortcuts to actually call the commands. the accelerators above just show the keyboard shortcuts
        #when you are in menu, binding them allows the user to actually use the shortcuts
        self.bind_all("<Command-o>", lambda event: self.after(100, self.onOpen))
        self.bind_all("<Command-Shift-s>", lambda event: self.after(100, self.onSaveAs))
        self.bind_all("<Command-s>", lambda event: self.after(100, self.onSave))
        self.bind_all("<Command-w>", lambda event: self.after(100, self.onQuit))
        self.bind_all("<Command-a>", lambda event: self.after(100, self.onSelectAll))
        self.bind_all("<Command-c>", lambda event: self.after(100, self.onCopy))
        self.bind_all("<Command-x>", lambda event: self.after(100, self.onCut))
        self.bind_all("<Command-v>", lambda event: self.after(100, self.onPaste))
        self.bind_all("<Command-p>", lambda event: self.after(100, self.onPrint))
        self.bind_all("<Command-Shift-f>", lambda event: self.after(100, self.onToggleFullScreen))
        self.bind_all("<Command-Shift-p>", lambda event: self.after(100, self.onCopyPath))
        self.bind_all("<Command-Option-i>", lambda event: self.after(100, self.onShowInfo))
        self.bind_all("<Command-Option-n>", lambda event: self.after(100, self.onWhatsNew))
        self.bind_all("<Command-Option-p>", lambda event: self.after(100, self.runPython))
        self.bind_all("<Command-Option-j>", lambda event: self.after(100, self.runJava))
        #adding an option to press escape when in fullscreen to go back to normal view
        self.bind_all("<Escape>", lambda event: self.after(100, self.escape))
        #this is where the right click is bound
        self.parent.bind("<Button-2>", self.showMenu)

        #adding a scrollbar along the right side of the window
        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.txt = Text(self, yscrollcommand=scrollbar.set)
        self.txt.pack(fill=BOTH, expand=1)
        #making the highlightthickness of the text widget be width of 0 so there is no border when selected
        #this makes the scroll bar look much better
        self.txt.config(bg=self.background, highlightthickness=0)
        #allow you to click and drag the scrollbar to move instead of using mouse scroll only
        scrollbar.config(command=self.txt.yview)
        """""""""""""""""
        BEGIN METHODS NOW
        """""""""""""""""
    def escape(self):
        if self.is_fullscreen:
            self.is_fullscreen = False
            unfullscreen(self.parent)

    #not yet working
    def onFont(self):
        mbox.showinfo("Not Implemented", "Unfotunately Typer does not currently support this function.")
    #not yet working
    def onFontSize(self):
        mbox.showinfo("Not Implemented", "Unfortunately Typer does not currently support this function.")
    #not yet working
    def onFontColor(self):
        mbox.showinfo("Not Implemented", "Unfotunately Typer does not currently support this function.")
    #shows the license in popup box
    def onLicense(self):
        #reading in the license text file
        l = self.readFile('LICENSE.txt')
        #displaying the license text file text in a showinfo box
        mbox.showinfo("License", l)
    #allows for running a python file from within Typer
    def runPython(self):
        if self.file_opened: #checks if a file is currently opened
            if str(self.current_file).endswith(".py"):  #if file opened, then check if it ends in .py as that would imply its a python file
                subprocess.call(['python', self.current_file]) #if it is a python file, then push a command to terminal to run it as python file
            elif str(self.current_file).endswith(".py") == False: #if it is not a python file
                mbox.showerror("Error", "Current opened file is not a Python file.") #show error that it is not python
        else:
            result = mbox.askquestion("Error", "No file is opened, would you like to open one to run now?") #if no file opened, ask if user would like to open one
            if result == 'yes':
                ftypes = [('Python files', '*.py')] #filetypes to be allowed to be open, notice its only python files allowed
                dlg = tkFileDialog.Open(self, filetypes=ftypes) #make a tkFileDialog box open allowing only files in ftypes to be opened (python files in this case)
                fl = dlg.show() #fl is path of file
                if fl != "": #fl is only "" if they cancel the selection
                    self.setTitle(fl) #sets title to file path
                    self.current_file = fl #sets current_file to the current path of file
                    text = self.readFile(fl) #reading in the file
                    self.txt.insert(END, text) #inserting text into the Typer field
                    self.file_opened = True #letting Typer know a file is opened
                    self.update() #forcing an update of Typer to display code
                    subprocess.call(['python', self.current_file]) #sending a command to terminal to run python file

    def runJava(self): #works exactly the same as python above, but looking for java files as opposed to python
        if self.file_opened:
            if str(self.current_file).endswith(".java"):
                subprocess.call(['javac', self.current_file])
            elif str(self.current_file.endswith(".java")) == False:
                mbox.showerror("Error", "Current opened file is not a Java file.")
        else:
            result = mbox.askquestion("Error", "No file is opened, would you like to open one to run now?")
            if result == 'yes':
                ftypes = [('Java files', '*.javac')]
                dlg = tkFileDialog.Open(self, filetypes=ftypes)
                fl = dlg.show()
                if fl != "":
                    self.setTitle(fl)
                    self.current_file = fl
                    text = self.readFile(fl)
                    self.txt.insert(END, text)
                    self.file_opened = True
                    self.update()
                    subprocess.call(['javac', self.current_file])

    def onSave(self): #allows for the current file to be saved/updated instead of having to save as every time
        if self.file_opened: #check if a file is even opened
            text = self.txt.get("1.0", END) #grab all the text from the Typer field
            subprocess.call(['rm', self.current_file]) #use terminal to remove/delete the file from the directory
            subprocess.call(['touch', self.current_file]) #now use terminal to make a new file with same name in same directory
            fi = open(self.current_file, 'w') #open the file
            fi.write(text) #write the text from before to the file, so the file is now updated with all the text that was there when save was selected

        else: #Detects that no file is opened, asks if they want to save as
            result = mbox.askquestion("Save as?", "There is currently no file for this text, would you like to save as?")
            if result == 'yes':
                self.onSaveAs() #calls onSaveAs if they want to save the file

    def onOpenSourceCode(self): #an option for people to view and edit the source code
        temp = self.txt.get("1.0", 'end-1c') #grab any text that may have been entered
        if temp == "": #check to see if any text is there. if not continue on with opening source code
            self.setTitle('Typer Source Code') #sets title to Typer Source Code
            text = self.readFile('typer.py') #reads in the source code to a text variable
            self.txt.insert(END, text) #inserts source code into Typer field
            self.file_opened = True #set file_opened to True
            self.current_file = 'typer.py' #set current_file to typer.py
        else: #if text is entered, ask them if they want to clear all text in favor of typer source code
            result = mbox.askquestion("Warning", "Opening the Typer source code will clear currently entered and unsaved text. Are you sure you want to open the Typer source code?")
            if result == 'yes': #if yes same process as above, if no then nothing happens
                self.txt.delete("1.0", END)
                self.setTitle('Typer Source Code')
                text = self.readFile('typer.py')
                self.txt.insert(END, text)
                self.file_opened = True
                self.current_file = "typer.py"

    def onWhatsNew(self): #a method to have a showinfo box explain changes from last version to current version. This should be updated anytime something is added.
        mbox.showinfo("What's New", "Added Background Color Chooser\n\nAdded What's New menu"
                                    "\n\nAdded typer.conf File to store defaults\n\nAdded a menu to view Typer Source Code"
                                    "\n\nAdded scrollbar along right side\n\nAdded Save option to update current file"
                                    "\n\nAdded a semi-functional fullscreen option\n\nAdded a way to open and run Java files"
                                    "\n\nAdded a way to open and run Python files\n\nWindow now centered upon opening"
                                    "\n\nAdded printing to default printer")

    def onBackground(self): #allows for the user to pick a background and possibly save it as their default background
        (rgb, hx) = tkColorChooser.askcolor() #built in color chooser from tkinter returns a tuple with rgb value and hex value
        if hx: #if there is a hex value (there is if they select a color and there is not if they press cancel)
            self.txt.config(bg=hx) #configure the Typer field to have background color of the users choice
            result = mbox.askquestion("Set as default?", "Would you like to set " + str(hx) + " as default background?") #asking to save as default
            if result == 'yes':
                conflist[0] = hx #conflist is a list of all lines on typer.conf, conflist[0] is first line, which is where background hex color is stored. If they want to update the default color, this gets changed to the hex they just chose
                subprocess.call(['rm', 'typer.conf']) #much like our save command, this removes/deletes typer.conf
                subprocess.call(['touch', 'typer.conf']) #and then re adds it
                newfile = open('typer.conf', 'w') #and opens the new typer.conf
                for x in conflist: #and rewrites it exactly as it was, with the exception of the first line hex value changing
                    newfile.write(x + "\n")

                mbox.showinfo("Saved", str(hx) + " has been saved as your default background!") #alerts the user that the color has been successfully changed/updated

    def onShowInfo(self): #simple method to showinfo about current version of Typer and some basic info about Typer
        mbox.showinfo("Typer Info", "Version: 0.0.1 Pre-Alpha \n\nLast Update: July 31 2016 \n\nDeveloped by Zach Purcell\n\nPrevious Version: N/A\n\nLicense: MIT License, see Info > License")

    def onPrint(self): #THIS METHOD WILL ONLY WORK IF YOU HAVE A DEFAULT PRINTER - IT PRINTS TO DEFAULT PRINTER
        text = self.txt.get("1.0", END)
        subprocess.call(['touch', 'tempfile.txt'])
        tempfile = open('tempfile.txt', 'r+')
        tempfile.write(text)
        subprocess.call(['lpr', 'tempfile.txt'])
        mbox.showinfo("Printing To Default Printer", "Printing to your default printer.")
        tempfile.close()

    def onCopyPath(self): #copies the current opened file path to clipboard
        if self.file_opened: #checks if a file is opened
            self.clipboard_clear() #clears the clipboard
            self.clipboard_append(str(self.current_file)) #appends the current_file to clipboard
        else:
            mbox.showerror("Error", "No file is opened so Typer cannot copy the file path.") #if no file opened, alert user

    def showMenu(self, e): #allows for right click menu to be shown
        self.menu.post(e.x_root, e.y_root)

    def onToggleFullScreen(self): #toggle fullscreen method
        if self.is_fullscreen: #checks if already fullscreen
            unfullscreen(self.parent) #if so, call unfullscreen method (located outside of class)
            self.is_fullscreen = False #and change is_fullscreen to false
        else:
            fullscreen(self.parent) #if not fullscreen, then call fullscreen method (located outside of class)
            self.is_fullscreen = True #and change is_fullscreen to True


    def setTitle(self, title): #allows for us to easily change the title of Typer
        self.parent.title(title)

    def onQuit(self): #when user presses Command+W or selects quit
        result = mbox.askquestion("Are you sure?", "Are you sure you want to quit?") #verifies with user that they want to quit
        if result == 'yes' and self.txt.get("1.0", 'end-1c') != "": #if yes but text is entered, ask if they want to save
            result = mbox.askquestion("Save?", "Would you like to save the open file?")
            if result == 'yes' and self.file_opened: #if file is opened, just save
                self.onSave()
                quit()
            elif result == 'yes' and self.file_opened == False: #if no file is opened, save as
                self.onSaveAs()
                quit()
            else: #if no, then just quit
                quit()
        elif result == 'yes' and self.txt.get("1.0", 'end-1c') == "":
            quit()

    def onOpen(self): #method to allow opening a file on users computer
        temp = self.txt.get("1.0", 'end-1c') #grabs any text in Typer field
        if temp == "": #if no text is entered
            ftypes = [('Python files', '*.py'), ('Text files', '*.txt'), ('Rich text files', '.rtf'), ('Java files', '*.java'), ('Conf files', '*.conf')] #these are current allowed files, can add any other text-type files though
            dlg = tkFileDialog.Open(self, filetypes = ftypes) #open the open file dialog
            fl = dlg.show() #grabs the path of the file selected
            self.setTitle(fl) #sets title as path of file selected
            self.current_file = fl #sets current file to the file selected

            if fl != '': #if a file is selected
                text = self.readFile(fl) #read the file selected and put it in text variable
                self.txt.insert(END, text) #insert the text in the Typer field
                self.file_opened = True #file opened is true

        elif temp != "": #if text is entered in Typer field
            result = mbox.askquestion("Warning", "Opening a new file will clear currently entered text. Are you sure you want to open another file?") #ask user if they want to open it
            if result == 'yes': #if they still want to open the new file, clear old text and put in file text
                self.txt.delete("1.0", END)
                ftypes = [('Python files', '*.py'), ('Text files', '*.txt'), ('Rich text files', '.rtf')]
                dlg = tkFileDialog.Open(self, filetypes = ftypes)
                fl = dlg.show()
                self.setTitle(fl)
                self.file_opened = True

                if fl != '':
                    text = self.readFile(fl)
                    self.current_file = str(fl)
                    self.txt.insert(END, text)

    def readFile(self, filename): #allows a simple call to return the text from a file
        f = open(filename, "r")
        text = f.read()
        self.current_file = f.name
        return text


    def onSaveAs(self): #allows user to save a file in any location as any acceptable name
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt") #allow them to save, default extension .txt though, can be changed
        self.current_file = f #set current file as saved name
        self.setTitle(self.current_file.name) #sets title
        if f is None: #if users cancels, do not continue
            return
        text_to_save = str(self.txt.get(1.0, END)) #grab text from Typer field
        f.write(text_to_save) #write it to th efile
        f.close() #close the file (in python, not in Typer)
        self.file_opened = True  #let Typer know a file is now opened

    def onSelectAll(self): #allows user to select all text intered in Typer field
        self.txt.tag_add(SEL, "1.0", END)
        self.txt.mark_set(INSERT, "1.0")
        self.txt.see(INSERT)

    def onCopy(self): #allows user to change the clipboard and copy text to it
        self.clipboard_clear()
        text = self.txt.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def onCut(self): #allows user to change the clipboard and cut text to it
        self.onCopy()
        self.txt.delete("sel.first", "sel.last")

    def onPaste(self): #allows user to grab text from clipboard and paste it in Type or anyother program for that matter
        text = self.clipboard_get()
        self.txt.insert("insert", text)


def fullscreen(Frame): #method to change size of window to fullscreen
    Frame.minsize(width=WIDTH,height=HEIGHT)
    Frame.attributes("-fullscreen", True)
    #code below performs same way
    """
    root.overrideredirect(1)
    root.geometry("%dx%d+0+0" % (WIDTH,HEIGHT))
    root.update()
    """


def unfullscreen(Frame): #method to change size of window to normal
    Frame.minsize(width=800,height=450)
    Frame.attributes("-fullscreen", False)
    #code below performs same way
    """
    root.overrideredirect(1)
    root.geometry("800x450+" + str(x) + "+" + str(y))
    """

if __name__ == '__main__': #start the program here
    root = Tk() #root = Tk() allows a window to be made
    root.title(typer_title) #this sets title of the window to typer_title, defined above the class
    ex = TyperClass(root) #an object named ex from TyperClass, takes root in as the frame for Typer
    WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight() #grabs the width and height from the screen
    x, y = WIDTH/4, HEIGHT/4 #sets x and y to 1/4 of each value so that the window can appear there and be centered
    root.geometry("800x450+" + str(x) + "+" + str(y)) #forces size of 800x450 using x and y as position of top left corner of window
    root.focus_set() #sets focus to window (does not work when called from terminal, no way around this as it is an OS thing)
    root.mainloop() #mainloop of root, allows program to run