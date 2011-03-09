# This file is part of the source code of
# gradint v0.9968 (c) 2002-2011 Silas S. Brown. GPL v3+.
#    This program is free software; you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation; either version 3 of the License, or
#    (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

# Start of users.py - multiple users in the Tk interface

settingsFile = "settings"+dottxt
user0 = (samplesDirectory,vocabFile,progressFile,progressFileBackup,pickledProgressFile,settingsFile)

def addUserToFname(fname,userNo):
  if not userNo or not fname: return fname
  elif os.sep in fname: return fname+"-user"+str(userNo)
  else: return "user"+str(userNo)+"-"+fname

def select_userNumber(N,updateGUI=1):
  global samplesDirectory,vocabFile,progressFile,progressFileBackup,pickledProgressFile,settingsFile
  prevUser = samplesDirectory
  samplesDirectory,vocabFile,progressFile,progressFileBackup,pickledProgressFile,settingsFile = user0
  samplesDirectory=addUserToFname(samplesDirectory,N)
  vocabFile=addUserToFname(vocabFile,N)
  progressFile=addUserToFname(progressFile,N)
  pickledProgressFile=addUserToFname(pickledProgressFile,N)
  settingsFile = addUserToFname("settings"+dottxt,N)
  if prevUser == samplesDirectory: return # called twice with same number
  ofl = firstLanguage
  if fileExists(settingsFile): readSettings(settingsFile)
  else: readSettings("settings"+dottxt) # the default one
  if not firstLanguage==ofl and updateGUI: # need to update the UI
      app.thin_down_for_lesson()
      app.todo.set_main_menu="keep-outrow"
  if updateGUI and hasattr(app,"vocabList"): del app.vocabList # re-read
def select_userNumber2(N):
    select_userNumber(N) ; app.userNo.set(str(N))

def setup_samplesDir_ifNec(d=0): # if the user doesn't have a samples directory, create one, and copy in the README.txt if it exists
  if not d: d=samplesDirectory
  if not isDirectory(d):
    os.mkdir(d)
    if fileExists(user0[0]+os.sep+"README"+dottxt): open(d+os.sep+"README"+dottxt,'wb').write(read(user0[0]+os.sep+"README"+dottxt))

def get_userNames(): # list of unicode user names or []
  ret=[]
  u=userNameFile ; c=0
  while fileExists(u):
    ret.append(unicode(u8strip(read(u)).strip(wsp),'utf-8'))
    c += 1 ; u=addUserToFname(userNameFile,c)
  global lastUserNames ; lastUserNames = ret
  return ret

def set_userName(N,unicodeName): open(addUserToFname(userNameFile,N),"w").write(unicodeName.encode("utf-8")+"\n") # implicitly adds if N=num+1

def wrapped_set_userName(N,unicodeName):
  if unicodeName.strip(wsp): set_userName(N,unicodeName)
  else: app.todo.alert="You need to type the person's name in the box before you press "+localise("Add new name") # don't waitOnMessage because we're in the GUI thread

GUI_usersRow = lastUserNames = None

def updateUserRow(fromMainMenu=0):
  row=GUI_usersRow
  if not row: return
  if hasattr(row,"widgetsToDel"):
    for w in row.widgetsToDel: w.pack_forget()
  row.widgetsToDel=[]
  names = get_userNames()
  if fromMainMenu and names==[""]:
    # someone pressed "add other students" but didn't add any - better reset it this run
    os.remove(userNameFile) ; names=[]
  if names:
    names.append("") # ensure at least one blank
    if not hasattr(app,"userNo"):
        app.userNo = Tkinter.StringVar(app)
        app.userNo.set("0")
    row["borderwidth"]=1
    if hasattr(Tkinter,"LabelFrame") and not winCEsound: # new in Tk 8.4 and clearer (but takes up a bit more space, so not winCEsound)
        r=Tkinter.LabelFrame(row,text=localise("Students"),padx=5,pady=5)
    else:
        r=addRow(row,1) ; Tkinter.Label(r,text=localise("Students")+":").grid(row=0,column=0,columnspan=2)
    row.widgetsToDel.append(r) ; row=r
    if winCEsound: row.pack()
    else: row.pack(padx=10,pady=10)
    global userBSM
    if len(names)>4:
        row, c = setupScrollbar(row,1) # better have a scrollbar (will configure it after the loop below)
        userBSM = ButtonScrollingMixin() ; userBSM.ourCanvas = c
    else: userBSM = None
    for i in range(len(names)):
      if names[i].strip(wsp):
        r=Tkinter.Radiobutton(row, text=names[i], variable=app.userNo, value=str(i), takefocus=0)
        r.grid(row=i+1,column=0,sticky="w")
        r["command"]=cmd=lambda e=None,i=i: select_userNumber(i)
        if not forceRadio:
           r2=Tkinter.Radiobutton(row, text="Select", variable=app.userNo, value=str(i), indicatoron=0) ; bindUpDown(r2,True)
           r2.grid(row=i+1,column=1,sticky="e")
           r2["command"]=cmd
           r2.bind('<Return>',lambda e=None,i=i: select_userNumber2(i))
           if userBSM: userBSM.bindFocusIn(r2)
        addButton(row,"Rename",lambda e=None,i=i,r=r,row=row:renameUser(i,r,row),"nopack").grid(row=i+1,column=2,sticky="e")
        r=addButton(row,"Delete",lambda e=None,i=i:deleteUser(i),"nopack") ; r.grid(row=i+1,column=3,sticky="e")
      else:
        r=Tkinter.Frame(row) ; r.grid(row=i+1,column=0,columnspan=4)
        text,entry = addTextBox(r)
        if not fromMainMenu: entry.focus() # because user has just pressed the "add other students" button, or has just added a name and may want to add another
        l=lambda *args:(wrapped_set_userName(i,asUnicode(text.get())),updateUserRow())
        addButton(r,localise("Add new name"),l)
        entry.bind('<Return>',l)
        if not i: Tkinter.Label(row,text="The first name should be that of the\nEXISTING user (i.e. YOUR name).").grid(row=i+2,column=0,columnspan=4)
      if userBSM: userBSM.bindFocusIn(r) # for shift-tab from the bottom
      if hasattr(row,"widgetsToDel"): row.widgetsToDel.append(r)
      if not names[i]: break
    if userBSM: c.after(cond(winCEsound,1500,300),lambda *args:c.config(scrollregion=c.bbox(Tkinter.ALL),width=c.bbox(Tkinter.ALL)[2],height=min(c["height"],c.winfo_screenheight()/2,c.bbox(Tkinter.ALL)[3]))) # hacky (would be better if it could auto shrink on resize)
  else: row.widgetsToDel.append(addButton(row,localise("Family mode (multiple user)"),lambda *args:(set_userName(0,""),updateUserRow())))

def renameUser(i,radioButton,parent,cancel=0):
    if hasattr(radioButton,"in_renaming"):
        del radioButton.in_renaming
        n=asUnicode(radioButton.renameText.get())
        if cancel: pass
        elif not n.strip(wsp) and len(lastUserNames)>1: tkMessageBox.showinfo(app.master.title(),"You can't have blank user names unless there is only one user.  Keeping the original name instead.")
        else:
            set_userName(i,n)
            radioButton["text"]=n
        radioButton.renameEntry.grid_forget()
        radioButton.grid(row=i+1,column=0,sticky="w")
    else:
        radioButton.in_renaming = 1
        radioButton.grid_forget()
        radioButton.renameText,radioButton.renameEntry = addTextBox(parent,"nopack")
        radioButton.renameEntry.grid(row=i+1,column=0)
        radioButton.renameText.set(lastUserNames[i])
        radioButton.renameEntry.focus()
        radioButton.after(10,lambda *args:radioButton.renameEntry.event_generate('<End>'))
        radioButton.renameEntry.bind('<Return>',lambda *args:renameUser(i,radioButton,parent))
        radioButton.renameEntry.bind('<Escape>',lambda *args:renameUser(i,radioButton,parent,cancel=1))

def deleteUser(i):
    for n in ["Are you sure","Are you REALLY sure","This is your last chance: Are you REALLY SURE"]:
        if not tkMessageBox.askyesno(app.master.title(),u""+n+" you want to delete "+lastUserNames[i]+" permanently, including any vocabulary list and recordings?"): return
    numUsers=len(lastUserNames)
    for fileOrDir in user0+(userNameFile,):
        d=addUserToFname(fileOrDir,i)
        if not d: continue # ??
        if isDirectory(d):
            while True:
                try: import shutil
                except: shutil = 0
                if shutil: shutil.rmtree(d,1)
                else: system(cond(winsound or mingw32,"del /F /S /Q \"","rm -rf \"")+d+"\"")
                if not isDirectory(d): break
                tkMessageBox.showinfo(app.master.title(),"Directory removal failed - make sure to close all windows etc that are open on it.")
        elif fileExists(d): os.remove(d)
        for j in range(i+1,numUsers):
            d2=addUserToFname(fileOrDir,j)
            if fileExists_stat(d2): os.rename(d2,d)
            d=d2
    select_userNumber2(0) # save confusion
    updateUserRow()
