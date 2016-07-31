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

        self.file_opened = False


    def TyperSetup(self):
        #using file_opened to determine if a file is currently open
        self.file_opened = False

        self.current_file = ""

        self.is_fullscreen = False

        self.parent.title(typer_title)
        self.pack(fill=BOTH, expand=1)

        #back = typerconf.next()
        #t = ""
        #for x in range(7):
        #    t += back[x]

        #self.background = t

        back = typerconf.readline()
        back = back.rstrip('\n')
        self.background = back

        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)

        fileMenu = Menu(menubar)
        fileMenu.add_command(label="Open", command=self.onOpen, accelerator="Command+o")
        fileMenu.add_command(label="Save As", command=self.onSaveAs, accelerator="Command+Shift+S")
        fileMenu.add_command(label="Save", command=self.onSave, accelerator="Command+S")
        fileMenu.add_command(label="Print", command=self.onPrint, accelerator="Command+P")
        menubar.add_cascade(label="File", menu=fileMenu)

        system = Menu(menubar)
        system.add_command(label="Quit", command=self.onQuit, accelerator="Command+w")
        system.add_command(label="Copy Path of File", command=self.onCopyPath, accelerator="Command+Shift+p")
        system.add_command(label="Toggle Fullscreen", command=self.onToggleFullScreen, accelerator="Command+Shift+f")
        menubar.add_cascade(label="System", menu=system)

        edit = Menu(menubar)
        edit.add_command(label="Select All", command=self.onSelectAll, accelerator="Command+a")
        edit.add_command(label="Cut", command=self.onCut, accelerator="Command+x")
        edit.add_command(label="Copy", command=self.onCopy, accelerator="Command+c")
        edit.add_command(label="Paste", command=self.onPaste, accelerator="Command+v")
        menubar.add_cascade(label="Edit", menu=edit)

        infoMenu = Menu(menubar)
        infoMenu.add_command(label="Show Info", command=self.onShowInfo, accelerator="Command+Option+I")
        infoMenu.add_command(label="What's new?", command=self.onWhatsNew, accelerator="Command+Option+N")
        infoMenu.add_command(label="Open Source Code", command=self.onOpenSourceCode)
        infoMenu.add_command(label="License", command=self.onLicense)
        menubar.add_cascade(label="Info", menu=infoMenu)

        personalize = Menu(menubar)
        personalize.add_command(label="Background", command=self.onBackground, accelerator="Command+Shift+B")
        menubar.add_cascade(label="Personalize", menu=personalize)

        run = Menu(menubar)
        run.add_command(label="Run Python File", command=self.runPython, accelerator="Command+Option+P")
        run.add_command(label="Run Java File", command=self.runJava, accelerator="Command+Option+J")
        menubar.add_cascade(label="Run", menu=run)

        doc = Menu(menubar)
        doc.add_command(label="Font", command=self.onFont)
        doc.add_command(label="Font Size", command=self.onFontSize)
        doc.add_command(label="Font Color", command=self.onFontColor)
        menubar.add_cascade(label="Document", menu=doc)

        self.menu = Menu(self.parent, tearoff=0)
        self.menu.add_command(label="Cut", command=self.onCut)
        self.menu.add_command(label="Copy", command=self.onCopy)
        self.menu.add_command(label="Paste", command=self.onPaste)

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
        self.parent.bind("<Button-2>", self.showMenu)

        scrollbar = Scrollbar(self)
        scrollbar.pack(side=RIGHT, fill=Y)

        self.txt = Text(self, yscrollcommand=scrollbar.set)
        self.txt.pack(fill=BOTH, expand=1)
        self.txt.config(bg=self.background, highlightthickness=0)

        scrollbar.config(command=self.txt.yview)

    def onFont(self):
        mbox.showinfo("Not Implemented", "Unfotunately Typer does not currently support this function.")

    def onFontSize(self):
        mbox.showinfo("Not Implemented", "Unfortunately Typer does not currently support this function.")

    def onFontColor(self):
        mbox.showinfo("Not Implemented", "Unfotunately Typer does not currently support this function.")

    def onLicense(self):
        l = self.readFile('LICENSE.txt')
        mbox.showinfo("License", l)

    def runPython(self):
        if self.file_opened:
            if str(self.current_file).endswith(".py"):
                subprocess.call(['python', self.current_file])
            elif str(self.current_file).endswith(".java") == False:
                mbox.showerror("Error", "Current opened file is not a Python file.")
        else:
            result = mbox.askquestion("Error", "No file is opened, would you like to open one to run now?")
            if result == 'yes':
                ftypes = [('Python files', '*.py')]
                dlg = tkFileDialog.Open(self, filetypes=ftypes)
                fl = dlg.show()
                if fl != "":
                    self.setTitle(fl)
                    self.current_file = fl
                    text = self.readFile(fl)
                    self.txt.insert(END, text)
                    self.file_opened = True
                    self.update()
                    subprocess.call(['python', self.current_file])

    def runJava(self):
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

    def onSave(self):
        if self.file_opened:
            print "if statement initiated"
            print self.current_file
            text = self.txt.get("1.0", END)
            subprocess.call(['rm', self.current_file])
            subprocess.call(['touch', self.current_file])
            fi = open(self.current_file, 'w')
            fi.write(text)

        else:
            result = mbox.askquestion("Save as?", "There is currently no file for this text, would you like to save as?")
            if result == 'yes':
                self.onSaveAs()

    def onOpenSourceCode(self):
        temp = self.txt.get("1.0", 'end-1c')
        if temp == "":
            self.setTitle('Typer Source Code')
            text = self.readFile('typer.py')
            self.txt.insert(END, text)
            self.file_opened = True
            self.current_file = 'typer.py'
        else:
            result = mbox.askquestion("Warning", "Opening the Typer source code will clear currently entered and unsaved text. Are you sure you want to open the Typer source code?")
            if result == 'yes':
                self.txt.delete("1.0", END)
                self.setTitle('Typer Source Code')
                text = self.readFile('typer.py')
                self.txt.insert(END, text)
                self.file_opened = True
                self.current_file = "typer.py"

    def onWhatsNew(self):
        mbox.showinfo("What's New", "Added Background Color Chooser\n\nAdded What's New menu"
                                    "\n\nAdded typer.conf File to store defaults\n\nAdded a menu to view Typer Source Code"
                                    "\n\nAdded scrollbar along right side\n\nAdded Save option to update current file"
                                    "\n\nAdded a semi-functional fullscreen option\n\nAdded a way to open and run Java files"
                                    "\n\nAdded a way to open and run Python files\n\nWindow now centered upon opening")

    def onBackground(self):
        (rgb, hx) = tkColorChooser.askcolor()
        if hx:
            self.txt.config(bg=hx)
            result = mbox.askquestion("Set as default?", "Would you like to set " + str(hx) + " as default background?")
            if result == 'yes':
                conflist[0] = hx
                subprocess.call(['rm', 'typer.conf'])
                subprocess.call(['touch', 'typer.conf'])
                newfile = open('typer.conf', 'w')
                for x in conflist:
                    newfile.write(x + "\n")

                mbox.showinfo("Saved", str(hx) + " has been saved as your default background!")

    def onShowInfo(self):
        mbox.showinfo("Typer Info", "Version: 0.0.1 Pre-Alpha \n\nLast Update: July 31 2016 \n\nDeveloped by Zach Purcell\n\nPrevious Version: N/A\n\nLicense: MIT License, see Info > License")

    def onPrint(self):
        mbox.showinfo("Not Implemented", "Unfotunately Typer does not currently support this function.")
        """ this will be worked on soon enough

        if self.file_opened:
            subprocess.call("lpr", self.current_file.name)
        else:
            result = mbox.askquestion("Error", "In order to print the file must be saved. Would you like to save now?")
            if result == "no":
                pass
            elif result == "yes":
                self.onSaveAs()
                subprocess.call("lp", self.current_file.name)
        """

    def onCopyPath(self):#currently not working
        mbox.showinfo("Not Implemented", "Unfotunately Typer does not currently support this function.")

    def showMenu(self, e):
        self.menu.post(e.x_root, e.y_root)

    def onToggleFullScreen(self):
        if self.is_fullscreen:
            fullscreen(self.parent)
            self.is_fullscreen = False
        else:
            unfullscreen(self.parent)
            self.is_fullscreen = True

    def setTitle(self, title):
        self.parent.title(title)

    def onQuit(self):
        result = mbox.askquestion("Are you sure?", "Are you sure you want to quit?")
        if result == 'yes' and self.txt.get("1.0", 'end-1c') != "":
            result = mbox.askquestion("Save?", "Would you like to save the open file?")
            if result == 'yes':
                self.onSaveAs()
                quit()
            else:
                quit()
        elif result == 'yes' and self.txt.get("1.0", 'end-1c') == "":
            quit()

    def onOpen(self):
        temp = self.txt.get("1.0", 'end-1c')
        if temp == "":
            ftypes = [('Python files', '*.py'), ('Text files', '*.txt'), ('Rich text files', '.rtf'), ('Java files', '*.java'), ('Conf files', '*.conf')]
            dlg = tkFileDialog.Open(self, filetypes = ftypes)
            fl = dlg.show()
            self.setTitle(fl)
            self.current_file = fl


            if fl != '':
                text = self.readFile(fl)
                self.txt.insert(END, text)
                self.file_opened = True

        elif temp != "":
            result = mbox.askquestion("Warning", "Opening a new file will clear currently entered text. Are you sure you want to open another file?")
            if result == 'yes':
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

    def readFile(self, filename):
        f = open(filename, "r")
        text = f.read()
        self.current_file = f.name
        return text


    def onSaveAs(self):
        f = tkFileDialog.asksaveasfile(mode='w', defaultextension=".txt")
        self.current_file = f
        self.setTitle(self.current_file.name)
        if f is None:
            return
        text_to_save = str(self.txt.get(1.0, END))
        f.write(text_to_save)
        f.close()
        self.file_opened = True

    def onSelectAll(self):
        self.txt.tag_add(SEL, "1.0", END)
        self.txt.mark_set(INSERT, "1.0")
        self.txt.see(INSERT)

    def onCopy(self):
        self.clipboard_clear()
        text = self.txt.get("sel.first", "sel.last")
        self.clipboard_append(text)

    def onCut(self):
        self.onCopy()
        self.txt.delete("sel.first", "sel.last")

    def onPaste(self):
        text = self.clipboard_get()
        self.txt.insert("insert", text)


def fullscreen(Frame):
    Frame.minsize(width=WIDTH,height=HEIGHT)
    Frame.attributes("-fullscreen", True)


def unfullscreen(Frame):
    Frame.minsize(width=1200,height=850)
    Frame.attributes("-fullscreen", False)

if __name__ == '__main__':
    root = Tk()
    root.title(typer_title)
    ex = TyperClass(root)
    WIDTH, HEIGHT = root.winfo_screenwidth(), root.winfo_screenheight()
    x, y = WIDTH/4, HEIGHT/4
    root.geometry("800x450+" + str(x) + "+" + str(y))
    root.mainloop()
