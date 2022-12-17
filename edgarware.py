import clamd
import os
import sys
import time
import colorama as c
import pyfiglet as fig

c.init()

edgar = """{}Edgar the Virus
Hunter

{}programmed entirely
in python in my room
by @LeWolfYT, clamd by Thomas Grainger
""".format(c.Fore.LIGHTYELLOW_EX, c.Fore.WHITE)

def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")
clear()

if not os.path.exists(os.path.expanduser("~/.edgar")):
    os.mkdir(os.path.expanduser("~/.edgar"))
    with open(os.path.expanduser("~/.edgar/lastsc"),"x"):
        pass
    with open(os.path.expanduser("~/.edgar/lastsc"),"a") as f:
        f.write("NEVER")
    with open(os.path.expanduser("~/.edgar/socketname"),"x"):
        pass
    with open(os.path.expanduser("~/.edgar/socketname"),"w") as f:
        f.write(input("clamd socket path: "))

#mac /usr/local/Cellar/clamav/0.105.1/sbin/clamd

with open(os.path.expanduser("~/.edgar/socketname"),"r") as f:
    h = f.read()
    cd = clamd.ClamdUnixSocket(path=os.path.expanduser(h))

print(edgar)

if cd.ping() != "PONG":
    print("Whoops! An error occured. Please restart the program and try again!")
    sys.exit()

os.system("sleep 3")
clear()

def getlasttime():
    h = None
    if os.path.exists(os.path.expanduser("~/.edgar/lastscan")):
        with open(os.path.expanduser("~/.edgar/lastscan","r")) as f:
            h = time.strftime(f.read())
    else:
        h = "NEVER"
    return h

prompt = """{}Virus Protection
version 1.1

{}Last scan was on {}.

""".format(c.Fore.LIGHTYELLOW_EX, c.Fore.WHITE, getlasttime())
print(prompt)
scantype = input("choose scan type (quick (default), full, dir, custom): ")

def scanning():
    print(c.Fore.LIGHTYELLOW_EX)
    print("scanning...")

found = []
foundfiles = []
def getscanstr(file, val):
    def addcommas(vals):
        if len(vals) == 1:
            return vals[0]
        else:
            stringout = ""
            for v in range(vals):
                if v == 0:
                    stringout += vals[v]
                else:
                    stringout += ", " + vals[v]
    value = list(val)
    if value[0] == 'OK':
        return None
    elif value[0] == 'FOUND':
        foundfiles.append(str(file))
        return str(file) + ": " +  addcommas(value[1:])
    else:
        return "ERROR ON FILE {}".format(file)
if scantype == "full":
    scanning()
    scan = cd.multiscan("/")
elif scantype == "dir":
    scandir = os.path.expanduser(input("scan directory: ")).replace("\\", "")
    if not os.path.exists(os.path.expanduser(scandir.replace("\\", "") )):
        while True:
            print("invalid path. please try again.")
            scandir = os.path.expanduser(input("scan directory: "))
            if os.path.exists(os.path.expanduser(scandir)):
                break
    scanning()
    scan = cd.multiscan(scandir)
elif scantype == "custom":
    folders = []
    while True:
        folderadd = input("Custom folder (s to start scanning): ")
        if folderadd == "s":
            break
        else:
            folders.append(folderadd)
    scan = {}
    for folder in folders:
        pass
else:
    def get_download_path():
        if os.name == 'nt':
            import winreg
            sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
            downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        else:
            return os.path.join(os.path.expanduser('~'), 'downloads')
    scanning()
    print("scanning downloads...")
    try:
        scan1 = cd.multiscan(get_download_path())
        print("done")
    except:
        scan1 = []
        print("error scanning downloads")
    print("scanning desktop...")
    try:
        scan2 = cd.multiscan(os.path.expanduser("~/Desktop/"))
        print("done")
    except:
        scan2 = []
        print("error scanning desktop")
    scan = {**scan1, **scan2}

with open(os.path.expanduser("~/.edgar/lastsc"), "w") as f:
    f.write(str(time.time()))

for fl in scan:
    if scan[fl][0] == "FOUND":
        found.append(getscanstr(fl,scan[fl])) #add strings
clear()
print("Scan Complete!")
f = fig.Figlet(font="Banner3")
if len(found) == 0:
    print(c.Fore.LIGHTBLUE_EX)
else:
    print(c.Fore.LIGHTRED_EX)
print(f.renderText(str(len(found))))
print(c.Fore.WHITE + "Viruses Found!\n")
if found == []:
    print("You're in the clear!")
else:
    for v in found:
        print(v)
    delete = input("Delete? (Y/n)")
    if not delete == "n":
        for file in foundfiles:
            os.remove(file)

cd.shutdown()