from cryptography.fernet import Fernet
import base64
from tkinter import * 
import mysql.connector as mysql
import time
import webbrowser
import sys, zipfile, os, dropbox, pytz
from threading import Event, Thread
from tkinter import Tk, ttk
from urllib.request import urlretrieve
from dropbox.files import FolderMetadata
from datetime import datetime, timezone

code = b"""
canread = True
candown = 0
lunmode = 0
votemode = 0
votetimleft = 0
imgwd = imght = imgx = imgy = 0
x = y = 0
votestat = 0
root = Tk()
root.resizable(0, 0)
i = 101
run = True
def quit():
    global run
    if (run):
        run = False

def fram(event):
    global i, candown
    i = 0
    candown = 2

def motion(event):
    global x, y
    x, y = event.x, event.y

def inrect(inx, iny, wdth, hght):
    global root, onrect
    root.bind('<Motion>', motion)
    xmaxpos = inx + wdth
    ymaxpos = iny + hght
    if (((x > xmaxpos) or (inx > x)) or ((y > ymaxpos) or (iny > y))):
        return False
    else:
        return True

def hover(mode, imgx, imgy):
    global lunmode, imgwd, imght, votemode
    onrect = inrect(imgx, imgy, imgwd, imght)
    if (mode == 0):
        if ((lunmode == 0) and (onrect)): ## lunmode says what img is on canvas now
            lunmode = 1
        if ((lunmode == 1) and not(onrect)):
            lunmode = 0
    if (mode == 1):
        if ((votemode == 0) and (onrect)): ## votemode says what img is on canvas now
            votemode = 1
        if ((votemode == 1) and not(onrect)):
            votemode = 0
def launchclicked():
        global candown, verconf, skipver, f, gamefile
        query = "SELECT version FROM indigomsver"
        cursor.execute(query,)
        records = cursor.fetchall()
        gamefile = records[0][0]+'.exe'
        candown = 4
            

def voteclicked(event):
        db = mysql.connect(
        host = "",
        user = "voter",
        passwd = "vote",
        database = "heavenms",

        )

        cursor = db.cursor()
        global votestat, ent, votetimeleft
        name = ent.get()
        query = "SELECT id,nxCredit,loggedin FROM accounts WHERE name = %s"
        cursor.execute(query, (name,))
        records = cursor.fetchall()
        if (records != []):
            accid = records[0][0]
            if (records[0][1] == None):
                idnx = 0
            else:
                idnx = records[0][1]
            logged = records[0][2]
            if (logged == 0):
                query = "SELECT IPadd FROM accips WHERE accId = %s"
                cursor.execute(query, (accid,))
                ipacc = cursor.fetchall()
                if (ipacc != []):
                    ipad = ipacc[0][0]
                    query = "SELECT votetime FROM vote WHERE IPadd = %s"
                    cursor.execute(query, (ipad,))
                    vtime = cursor.fetchall()
                    timenow = round(time.time())
                    if (timenow - vtime[0][0] > 86400):
                        query = "UPDATE vote SET votetime = %s WHERE IPadd = %s"
                        query1 = "UPDATE accounts SET nxCredit = %s WHERE id = %s"
                        idnx += 5000
                        val = (timenow,ipad)
                        val1 = (idnx,accid)
                        cursor.execute(query, val)
                        cursor.execute(query1, val1)
                        db.commit()
                        webbrowser.open("https://gtop100.com/topsites/MapleStory/sitedetails/IndigoMS-Launched-on-18821-x6-exp--x3-drop--x2-meso-Open-Beta-rates-100007?vote=1")
                        votestat = 1
                    else:
                        votetimeleft = round((vtime[0][0]+86400-timenow)/60)
                        votestat = 2
                else:
                    votestat = 3
            else:
                votestat = 4
        else:
            votestat = 5


root.title("IndigoMS Launcher")
root.iconbitmap('maple.ico')

canvas1 = Canvas(root,width = 300, height = 300, relief = FLAT, background = "#D2D2D2")
canvas1.pack()

db = mysql.connect(
    host = "",
    user = "voter",
    passwd = "vote",
    database = "heavenms",

    )

cursor = db.cursor()

query = "SELECT loggedin FROM accounts"
cursor.execute(query,)
myresult =  cursor.fetchall()
indx = 0
players = 0
while (indx < len(myresult)):
    if(myresult[indx][0] == 2):
        players += 1
    indx += 1

query = "SELECT status FROM indigomsver"
cursor.execute(query,)
records = cursor.fetchall()
serverstatus = int(records[0][0])

imgbgn = PhotoImage(file="maplestory.png")
imglunpres = PhotoImage(file="plyunpre.png")
imglunc = PhotoImage(file="plypre.png")
imgvotepres = PhotoImage(file="voteunpre.png")
imgvote = PhotoImage(file="votepre.png")
frame = PhotoImage(file="fram.png")
imgwd = imglunpres.width()
imght = imglunpres.height()
ent = Entry(root, width=17)
ent.configure({"background": "white"})
timestart = round(time.time())
while run:
    timern = round(time.time())
    if (i == 100):
        candown = 1
        launchclicked()
    i += 1
    root.protocol("WM_DELETE_WINDOW", quit)
    imgrectbgn = canvas1.create_image(0,0, anchor=NW, image=imgbgn)
    framerect = canvas1.create_image(55,95, anchor=NW, image=frame)
    canvas1.tag_bind(imgrectbgn)
    canvas1.tag_bind(framerect)
    if (serverstatus == 0):
        user_window_lab = canvas1.create_text(235 ,10, anchor = "nw",text="Offline", fill='red',font=("Times New Roman", 15))
    else:
        user_window_lab = canvas1.create_text(235 ,7, anchor = "nw",text="Online", fill='blue',font=("Times New Roman", 15))
    user_window_lab = canvas1.create_text(255 ,32, anchor = "nw",text=str(players), fill='blue',font=("Times New Roman", 15))
    user_window_ent  = canvas1.create_window(10 ,195, anchor = "nw", window = ent)
    overlaunch = False
    if (lunmode == 0):
        hover(0, 15,260)
        imgrectlunpres = canvas1.create_image(15,260, anchor=NW, image=imglunpres)
        canvas1.tag_bind(imgrectlunpres) ## same, but for the text.
    else:
        hover(0, 15,260)
        imgrectlun = canvas1.create_image(15,260, anchor=NW, image=imglunc)
        canvas1.tag_bind(imgrectlun, "<Button-1>", fram) ## same, but for the text.
    if (votemode == 0):
        hover(1, 15, 220)
        imgrectvotepres = canvas1.create_image(15,220, anchor=NW, image=imgvotepres)
        canvas1.tag_bind(imgrectvotepres) ## same, but for the text.
    else:
        hover(1, 15, 220)
        imgrectvote = canvas1.create_image(15,220, anchor=NW, image=imgvote)
        canvas1.tag_bind(imgrectvote, "<Button-1>", voteclicked) ## same, but for the text.
    if (candown == 1):
        user_window_lab = canvas1.create_text(60 ,100, anchor = "nw",text="game files out-dated", fill='red',font=("Times New Roman", 15,'bold'))
    if (candown == 0):
        tz = pytz.timezone('Europe/Athens')
        athens_now = datetime.now(tz)
        user_window_lab = canvas1.create_text(60 ,100, anchor = "nw",text="Server time: "+athens_now.strftime("%H:%M:%S"), fill='red',font=("Times New Roman", 14,'bold'))
    if (candown == 2):
        user_window_lab = canvas1.create_text(100 ,100, anchor = "nw",text="Launching...", fill='purple',font=("Times New Roman", 15,'bold'))
    if (candown == 3):
        user_window_lab = canvas1.create_text(115 ,100, anchor = "nw",text="Ready!", fill='purple',font=("Times New Roman", 15,'bold'))
    if (candown == 4):
        print(gamefile)
        os.startfile(gamefile)
        candown = 3
    if (votestat == 0):
        user_window_lab = canvas1.create_text(20 ,165, anchor = "nw",text="Please enter", fill='blue',font=("Times New Roman", 10))
        user_window_lab = canvas1.create_text(20 ,177, anchor = "nw",text="account name:", fill='blue',font=("Times New Roman", 10))
    if (votestat == 1):
        user_window_lab = canvas1.create_text(20 ,165, anchor = "nw",text="Please solve", fill='blue',font=("Times New Roman", 10))
        user_window_lab = canvas1.create_text(20 ,177, anchor = "nw",text="the puzzle!", fill='blue',font=("Times New Roman", 10))
    if (votestat == 2):
        user_window_lab = canvas1.create_text(13 ,166, anchor = "nw",text="Already voted!", fill='red',font=("Times New Roman", 10))
        user_window_lab = canvas1.create_text(13 ,177, anchor = "nw",text="time left:"+str(votetimeleft)+" mins", fill='red',font=("Times New Roman", 10))
    if (votestat == 3):
        user_window_lab = canvas1.create_text(20 ,165, anchor = "nw",text="Error while", fill='red',font=("Times New Roman", 10))
        user_window_lab = canvas1.create_text(20 ,177, anchor = "nw",text="extracting data!", fill='red',font=("Times New Roman", 10))
    if (votestat == 4):
        user_window_lab = canvas1.create_text(10 ,166, anchor = "nw",text="Account is logged in", fill='red',font=("Times New Roman", 10))
        user_window_lab = canvas1.create_text(10 ,177, anchor = "nw",text="please log off!", fill='red',font=("Times New Roman", 10))
    if (votestat == 5):
        user_window_lab = canvas1.create_text(20 ,166, anchor = "nw",text="Account name", fill='red',font=("Times New Roman", 10))
        user_window_lab = canvas1.create_text(20 ,177, anchor = "nw",text="is wrong!", fill='red',font=("Times New Roman", 10))
    if ((timern-timestart > 300) and (candown != 2)):
        run = False
    root.update_idletasks()
    root.update()
"""

key = Fernet.generate_key()
encryption_type = Fernet(key)
encrypted_message = encryption_type.encrypt(code)

decrypted_message = encryption_type.decrypt(encrypted_message)

exec(decrypted_message)