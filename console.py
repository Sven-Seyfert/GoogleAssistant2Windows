#import libraries and modules for console
import tkinter
from general import  *
from queue import Queue

#import libraries and modules for trayicon
import pystray
import os
from PIL import Image, ImageDraw


""" Functions for the console """

q = Queue ()

def log (message, mprefix=0, time=0, userinput=False, guitext=0):
    if time == 0:
        time = current_time()

    if guitext == 0:
        guitext = console_output

    if mprefix == 1:
        sprefix = "[" + time + "]\t"
    elif mprefix == 2:
        sprefix = ">   "
    elif mprefix == 3:
        sprefix = "     "
    else:
        sprefix = ""

    guitext.configure(state='normal')
    if userinput == True:
        guitext.insert ("end", sprefix + "<" + message + ">\n")
    else:
        guitext.insert ("end", sprefix + message + "\n")
    guitext.configure(state='disabled')

def process_cmd(event):
    cmd = console_prompt.get()
    console_prompt.delete(0, 'end')

    if cmd == "":
        return

    log (cmd, 1, userinput=True)
    if cmd =="hide":
        hide_console()
    elif cmd=="stop" or cmd=="quit":
        terminate()
    else:
        log ("Unknown command. Type <help> for more information.", 2)
        return

def hide_console():
    consoleGUI.withdraw()
    log ("Hid the console", 2)
    trayicon.run ()

def restore_console ():
    #print ("console restored")
    consoleGUI.deiconify()
    delete_trayicon ()
    log ("Console restored", 1)

def terminate():
    log("Shutting down console", 2)
    consoleGUI.after (1000, consoleGUI.destroy)
    #consoleGUI.destroy()

def create_console_GUI ():
    console_font = "Segoe 9"

    global consoleGUI
    global console_output
    global console_prompt
    #print ("declared global variables")

    consoleGUI = tkinter.Tk()
    consoleGUI.title ("GoogleAssistant2Windows Console")
    consoleGUI.iconbitmap(default=".files\\GA2W-logo.ico")
    consoleGUI.resizable(False, False)
    consoleGUI.geometry("800x265")
    consoleGUI.configure (bg="white")

    console_output = tkinter.Text (consoleGUI, bg="white", height=15, bd=1,
        font=console_font, borderwidth = 1, relief="solid")
    console_output.configure(state='disabled')
    q.put(console_output)

    console_prompt = tkinter.Entry (consoleGUI, bd=0, font=console_font, borderwidth = 1, relief="solid")


    console_output.pack (fill="x", padx=5, pady=5)
    console_prompt.pack (fill="x", padx=5)

    consoleGUI.bind('<Return>', process_cmd)
    consoleGUI.protocol("WM_DELETE_WINDOW", hide_console)

    #consoleGUI.mainloop()

def start_console_GUI():
    consoleGUI.mainloop()

""" Functions for the trayicon """

def create_trayicon ():

    cwd = os.getcwd()
    iconpath = cwd + "\\.files\\GA2W-logo.png"

    global trayicon

    trayicon = pystray.Icon('GA2W-Traymenu', trayicon_create_image(iconpath), menu=pystray.Menu(
        pystray.MenuItem ('Restore Console', restore_console  )))

def delete_trayicon ():
    trayicon.stop ()

def trayicon_create_image(imagepath):
    image = Image.open (imagepath)
    return image


def main():

    #prepare the GUI and the trayicon
    create_console_GUI()
    guitext = q.get()
    q.task_done()

    create_trayicon ()

    #start the mainloop
    start_console_GUI()



if __name__ == '__main__':
    main()

    global guitext
    guitext = q.get()
    q.task_done()
