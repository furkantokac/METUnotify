#!/usr/bin/python

import mechanize, os, data, wx, sys, time
from webbrowser import open

print "-----------------------------------"
os.chdir(os.path.dirname(os.path.abspath(sys.argv[0])))

print "P.ID:",os.getpid()

username  = data.getup(0)
password  = data.getup(1)

browser = mechanize.Browser()
browser.set_handle_robots(False)

reFreq = 60 # Refresh frequency as second
iconself = "the variable will be global reference of class"

def checkConnection(reference="https://login.metu.edu.tr/cas/login"):
   print "checkConnection " + reference
   #try:
   browser.open(reference)
   return 1
   #except:
   pass
   
   iconself.ShowBalloon("Connection Failed", "Please check internet connection.", 3)
   print "Connection Failed"
   time.sleep(5)
   iconself.RemoveIcon()
   sys.exit(0)

def checkLogin():
   if not loginQuota():
      print "Login failed."
      iconself.ShowBalloon("Login Fail", "Please check username and password.", 3)
      time.sleep(5)
      iconself.RemoveIcon()
      sys.exit(0)
   
   return 1

# Returns list of numbers in string
# Will be used to handle websites codes
def returnNums(s):
   s += "END"
   num = ""
   numList = []
   flag = False
   for c in s:
      if c.isdigit():
         num+=c
         flag = True
      elif flag:
         numList.append(num)
         flag = False
         num = ""
   return numList

def loginEmail():
   try:
      #checkConnection("https://horde.metu.edu.tr/login.php")
      browser.open("https://horde.metu.edu.tr/login.php")
      browser.select_form(nr = 0)
      browser.form['horde_user'] = username
      browser.form['horde_pass'] = password
      resp = browser.submit()
      print "Email login successful."
      resp = resp.read() # if "frameset" in resp: SUCCESSFULL
      return 1
   except:
      print "Email login failed. Exit"
      iconself.ShowBalloon("Login Fail", "Email login failed. Try again.", 3)
      sys.exit(0)
   print "Email login fail."
   return 0 # fail

def loginQuota():
   try:
      #checkConnection("https://login.metu.edu.tr/cas/login")
      browser.open("https://login.metu.edu.tr/cas/login")
      browser.select_form(nr = 0)
      browser.form['username'] = username
      browser.form['password'] = password
      resp = browser.submit()
      resp = resp.read() # if "successful" in resp:
      print "Quota login successfull."
      return 1
   except:
      pass
   print "Quota login fail."
   return 0 # fail

def checkMail(): # Returns number of new email/s
   print "checkMail"
   
   try:
      resp = browser.open('https://horde.metu.edu.tr/imp/mailbox.php?no_newmail_popup=1&mailbox=INBOX')
      contents = resp.read()
      newMsg = contents.split('"ltr">Gelen Kutusu')[1]
      newMsg = returnNums(newMsg[:10])
      
      checkEmailFailed = 0
      if newMsg:
         return newMsg[0]
      else:
         return "0"
   except:
      pass
   
   loginEmail()
   try:
      resp = browser.open('https://horde.metu.edu.tr/imp/mailbox.php?no_newmail_popup=1&mailbox=INBOX')
      contents = resp.read()
      newMsg = contents.split('"ltr">Gelen Kutusu')[1]
      newMsg = returnNums(newMsg[:10])
      
      checkEmailFailed = 0
      if newMsg:
         return newMsg[0]
      else:
         return "0"
   except:
      iconself.ShowBalloon("Connection Problem", "Please check internet connection.", 3)
      sys.exit(0)

def leftQuota():
   try:
      print "leftQuota"
      resp = browser.open('http://net.ncc.metu.edu.tr/kota/kota_intranet.php')
      resp = resp.read()
      resp = resp.split("(approximately) ")[1]
      resp = resp.split(".")[0]
      checkQuotaFailed = 0
      return resp
   except:
      pass
   
   loginQuota()
   try:
      print "leftQuota"
      resp = browser.open('http://net.ncc.metu.edu.tr/kota/kota_intranet.php')
      resp = resp.read()
      resp = resp.split("(approximately) ")[1]
      resp = resp.split(".")[0]
      checkQuotaFailed = 0
      return resp
   except:
      return -1
   
# When pressed checknow, check email and do what it should do
# if everything is ok, return 1
def handleCheck():
   newMail = int(checkMail())
   print "You have", newMail, "new mail."
   if newMail == 0:
      iconself.ShowBalloon("No New Mail", "There is no unread mail.")
   else:
      iconself.ShowBalloon("New Mail", (str(newMail)+" unread mail."))
   return 1

# When pressed checkquota, check quota and do what it should do
# if everything is ok, return 1
def handleQuota():
   lq = leftQuota()
   if lq == -1:
      iconself.ShowBalloon("Connection Problem", "Please check internet connection.", 3)
      return 0
   else:
      iconself.ShowBalloon("Left Quota", lq, 1)
      print "Left quota ", lq
      return 1

# Make routine check when autocheck enabled
# if everything is ok, return 1
def handleChecking():
   newMail = int(checkMail())
   print "You have", newMail, "new mail."
   
   '''if newMail > 0:
      iconself.set_icon("4")
   else:
      iconself.set_icon("1")'''
   
   return 1
# it handle delay and things which should be done during delay when autocheck enabled
def handleDelay():
   timeout = time.time() + reFreq
   while timeout > time.time():
      handleCheck()
      handleQuota()
def startAutoChecking(self):
   '''
   while True:
      handleChecking()
      handleIcon()
      handleDelay()
      print reFreq,"sec passed. Refreshing...\n"
      print ""
   '''

# main function
def main():
   global iconself
   
   app = wx.App(False)
   iconself = TaskBarIcon()
   # if internet/login connection fails, program kills itself
   iconself.ShowBalloon("Check", "Connection checking...")
   checkConnection()
   iconself.ShowBalloon("Login", "Logging in to accounts...")
   checkLogin()
   iconself.ShowBalloon("Ready!", "METUnotify is ready to use.")
   app.MainLoop()

currentIcon = "1"   

#------------------CLASSES--------------------
def create_menu_item(menu, label, func):
    item = wx.MenuItem(menu, -1, label)
    menu.Bind(wx.EVT_MENU, func, id=item.GetId())
    menu.AppendItem(item)
    return item
    
class TaskBarIcon(wx.TaskBarIcon):
   def __init__(self):
      super(TaskBarIcon, self).__init__()
      self.set_icon("1")
      self.Bind(wx.EVT_TASKBAR_LEFT_DOWN, self.on_left_down)
   
   def CreatePopupMenu(self):
      menu = wx.Menu()
      #create_menu_item(menu, 'Check Mail Now', self.on_mailCheck)
      create_menu_item(menu, 'Check Quota', self.on_quotaCheck)
      create_menu_item(menu, 'Go Inbox', self.on_goInbox)
      menu.AppendSeparator()
      create_menu_item(menu, 'Quit', self.on_quit)
      create_menu_item(menu, 'About', self.on_about)
      return menu

   def set_icon(self, iconNo):
      path = '.\iconIco\\' + iconNo + '.ico'
      currentIcon = iconNo
      icon = wx.IconFromBitmap(wx.Bitmap(path))
      self.SetIcon(icon, 'METUnotify')
   
   def on_left_down(self, event):
      print 'Tray icon was left-clicked.'
      iconself.ShowBalloon("Check", "Quota checking...")
      handleQuota()
	
   def on_mailCheck(self, event):
      print "Clicked Mailcheck"
      handleCheck()
   
   def on_quotaCheck(self, event):
      print "Clicked Quotacheck"
      iconself.ShowBalloon("Check", "Quota checking...")
      handleQuota()
   
   def on_goInbox(self, event):
      print 'Clicked Goinbox'
      open("https://horde.metu.edu.tr/imp/mailbox.php?mailbox=INBOX&sortdir=0&sortby=0&actionID=change_sort")
   
   def on_quit(self, event):
      print 'on_quit'
      self.RemoveIcon()
      wx.CallAfter(self.Destroy)
	
   def on_about(self, event):
      print 'Clicked About'
      self.ShowBalloon("About", "________________\nMETUnotify V0.0\nDev : Furkan TOKAC")

if __name__ == "__main__":
   main()
