# typer-repo
I am aiming to make Typer a open-source, free to use, and editable text editor. It is currently in development and is written
and tested for Apple Mac computers. Although any Unix system should be similar, I have not tested it on one yet. Eventually I
will make a Windows version, as it should only be a few small changes (thanks python!).

Once you obtain typer.py and typer.conf they must be in the same directory (as of now) in order to work. This is because typer.conf
stores default settings for Typer that allows it to not have to be reset each time. Eventually I am going to add in a method that checks if the config file is there and creates a default one if not, which will allow for only typer.py to be needed at first. Eventually going to do something like py2app to make Typer an application as opposed to just a python file.

Typer is also going to eventually be a simple programming tool, as it already includes a way to run Python and Java files from
within the application itself.

KNOWN BUGS:
Fullscreening (on a mac) allows for the window to be dragged around the screen but keep its size. This is an issue (obviously), as
  we would prefer it to be immoblie. Have not found much in terms of making the window stay put, but looking into the issue. Also first time fullscreen is toggled it does not engage and window changes size. The window changing size is hardcoded in but the fact that it doesn't work first time but does every time after is an issue I will be working on.

TROUBLE PRINTING?
If you are having trouble printing please verify that you have a default printer selected. Go to System Preferences -> Printers & Scanners -> right click preferred printer and select set as default
Try printing again! Make sure that if it is a network printer that you are on the proper network, and if it is local make sure it is plugged into your computer!

LICENSE:
See LICENSE.txt for a rundown on this. TL;DR: MIT license, free to use and edit anyway you want as long as you give credit to me
(Zach Purcell) and accept that no liability falls on me for any problems that arise due to the program in its current state or
edited-by-you state. Once again, for a full rundown please see LICENSE.txt
