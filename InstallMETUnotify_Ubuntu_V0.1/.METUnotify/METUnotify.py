#!/usr/bin/python
import mechanize
import subprocess, data, os
from time import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Check if user trying to open more than 2 program at the same time
output = os.popen("cat /proc/"+data.get("pid")+"/cmdline").read()
if "METUnotify" in output:
   os.system('notify-send -i /usr/share/icons/METUnotifyIcons/fail.png "Already Running" "Your program already running."')
   exit(0)

data.setAllZero()
data.set("pid", str(os.getpid()))
print "P.ID:",os.getpid()

username  = data.getup(0)
password  = data.getup(1)
browser = mechanize.Browser()
reFreq = 60 # Refresh frequency as second
icon = 1 
ka = 0 # Will be variable of subprocess of appIndicator.py

def checkConnection(reference='https://horde.metu.edu.tr/'):
   try:
      browser.open(reference)
      return 1
   except:
      pass
   
   os.system('notify-send -i /usr/share/icons/METUnotifyIcons/fail.png "Connection Fail" "Please check internet connection."')
   print "Connection Fail\nPlease check internet connection."
   exit(0)

def checkLogin():
   if not loginAccounts():
      os.system('notify-send -i /usr/share/icons/METUnotifyIcons/fail.png "Login Fail" "Please check username and password."')
      print "Login failed.\nPlease check username and password."
      exit(0)
   return 1

def returnNums(s):# Returns list of numbers in string
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

def loginAccounts(): # Return 1 if login successful
   print "loginAccounts"
   # EMAIL LOGIN
   browser.open("https://horde.metu.edu.tr/login.php")
   browser.select_form(nr = 0)
   browser.form['horde_user'] = username
   browser.form['horde_pass'] = password
   resp = browser.submit()
   resp = resp.read()
   
   if not "frameset" in resp:
      print "Email login fail."
      return 0 # fail
   
   # QUOTA LOGIN
   browser.open("https://login.metu.edu.tr/cas/login")
   browser.select_form(nr = 0)
   browser.form['username'] = username
   browser.form['password'] = password
   resp = browser.submit()
   resp = resp.read()
   
   if not "successful" in resp:
      print "Quota login fail."
      return 0 # fail
   else:
      print "Quota and Email login successfull."
      return 1 # successfull
   

def checkMail(): # Returns number of new email/s
   print "checkMail"
   
   resp = browser.open('https://horde.metu.edu.tr/imp/mailbox.php?no_newmail_popup=1&mailbox=INBOX')
   contents = resp.read()
   newMsg = contents.split('"ltr">Gelen Kutusu')[1]
   newMsg = returnNums(newMsg[:10])
   
   if newMsg:
      return newMsg[0]
   else:
      return "0"

def leftQuota():
   print "leftQuota"
   #checkConnection('http://net.ncc.metu.edu.tr/kota/kota_intranet.php')
   resp = browser.open('http://net.ncc.metu.edu.tr/kota/kota_intranet.php')
   resp = resp.read()
   resp = resp.split("(approximately) ")[1]
   resp = resp.split(".")[0]
   os.system('notify-send -i /usr/share/icons/METUnotifyIcons/quota.png "Left Quota" "'+resp+'"')
   print "left quota", resp
   return resp

# When pressed checknow, check email and do what it should do
# if everything is ok, return 1
def handleCheck():
   global icon
   
   check = int(data.get("check"))
   if check == 1:
      data.set("check", 0)
      print "check set 0"
      
      newMail = int(checkMail())
      
      if newMail == 0:
         icon = 1
      else:
         icon = 4
      
      if newMail == 0:
         os.system('notify-send -i /usr/share/icons/METUnotifyIcons/email.png "No New Mail" "There is no new mail."')
      else:
         os.system('notify-send -i /usr/share/icons/METUnotifyIcons/email.png "New Mail" "'+str(newMail)+' unread mail."')
   return 1

# Make routine check of email
# if everything is ok, return 1
def handleChecking():
   global icon
   
   newMail = int(checkMail())
   print "You have", newMail, "new mail."
   if newMail > 0:
      icon = 4
   else:
      icon = 1
   
   return 1

# When pressed checkquota, check quota and do what it should do
# if everything is ok, return 1
def handleQuota():
   quota = int(data.get("quota"))###
   if quota == 1:
      data.set("quota", 0)
      print "quota set 0"
      leftQuota()
   return 1

# Check if icon should be change or not, then do what it should do
# if everything is ok, return 1
def handleIcon():
   global icon
   global ka
   
   cicon = int(data.get("icon"))
   if not cicon == icon:
      data.set("icon", icon)
      print "Icon set", icon
      ka.kill()
      ka = subprocess.Popen(['python', 'appIndicator.pyc'])
   return 1

# it handle delay and things which should be done during delay
def handleDelay():
   timeout = time() + reFreq
   while timeout > time():
      handleCheck()
      handleIcon()
      handleQuota()
   
# main function
def main():
   # if internet/login connection fails, program kill itself
   checkConnection()
   checkLogin()
   
   global ka # subprocess of appIndicator.py
   ka = subprocess.Popen(['python','appIndicator.pyc'])
   
   while True:
      handleChecking()
      handleIcon()
      handleDelay()
      print reFreq,"sec passed. Refreshing...\n"

if __name__ == "__main__":
   main()
