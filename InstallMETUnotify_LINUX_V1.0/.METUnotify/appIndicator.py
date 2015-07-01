#!/usr/bin/python
from os import path, system, chdir, popen
import appindicator, gtk, data
from webbrowser import open

# This function kill appIndicator if METUnotify is not running.
# Especially, this is necessary when starting system from hibernate
def controlmain():
   output = popen("cat /proc/"+data.get("pid")+"/cmdline").read()
   if not "METUnotify" in output:
      system('notify-send -i /usr/share/icons/METUnotifyIcons/fail.png "Connection Problem" "Please restart program."')
      print "METUnotify not running. Quit appIndicator."
      exit(0)

controlmain()

chdir(path.dirname(path.abspath(__file__)))
icon = '/usr/share/icons/METUnotifyIcons/' + data.get("icon") + '.png'
myInd = appindicator.Indicator('METUnotify', icon, appindicator.CATEGORY_APPLICATION_STATUS)
myInd.set_status( appindicator.STATUS_ACTIVE )
m = gtk.Menu()

btnCheck = gtk.MenuItem( 'Check Mail Now' )
btnQuota = gtk.MenuItem( 'Check Quota' )
btnGolink = gtk.MenuItem( 'Go Inbox' )
btnQuit = gtk.MenuItem( 'Quit' )
btnAbout = gtk.MenuItem( 'About' )

m.append(btnCheck)
m.append(btnQuota)
m.append(btnGolink)
m.append(btnQuit)
m.append(btnAbout)

myInd.set_menu(m)
btnCheck.show()
btnQuota.show()
btnGolink.show()
btnQuit.show()
btnAbout.show()

def mailCheck(item):
   controlmain()
   data.set("check", 1)
   print "check set 1"

def quotaCheck(item):
   controlmain()
   data.set("quota", 1)
   print "quota set 1"

def goMailPage(item):
   controlmain()
   open("https://horde.metu.edu.tr/imp/mailbox.php?mailbox=INBOX&sortdir=0&sortby=0&actionID=change_sort")

def quit(item):
   pid = data.get("pid")
   # if TRUE, it means there is no opened METUnotify.py so don't kill process
   output = popen("cat /proc/"+pid+"/cmdline").read()
   if "METUnotify" in output:
      print "Process "+pid+" kill."
      system("kill "+ pid)
   gtk.main_quit()

def about(item):
   system('notify-send -i /usr/share/icons/METUnotifyIcons/dev.png "Developer & Contact" "furkan.tokac@metu.edu.tr\nfurkantokac.blogspot.com"')

btnCheck.connect('activate', mailCheck)
btnQuota.connect('activate', quotaCheck)
btnGolink.connect('activate', goMailPage)
btnQuit.connect('activate', quit)
btnAbout.connect('activate', about)

gtk.main()
