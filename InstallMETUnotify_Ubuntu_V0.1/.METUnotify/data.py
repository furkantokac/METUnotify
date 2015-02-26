#!/usr/bin/python

defaultStr = "pid.0.check.0.quota.0.icon.1.quit.0.mail.0."
fileName = "data.txt"

def get(item):
   fo = open(fileName, "r")
   ret = fo.read()
   fo.close()
   
   if not item in ret:
      return -1
   
   ret = ret.split('.')
   i = ret.index(item)
   return str(ret[i+1])

def set(item, value):
   value = str(value)
   fo = open(fileName, "r")
   data = fo.read()
   fo.close()
   
   if not item in data:
      return -1
   
   data = data.split(".")
   i = data.index(item)
   data[i+1] = value
   ret = '.'.join(data)
   
   fo = open(fileName, "w")
   fo.write(ret)
   fo.close()
   
   return 1

def setAllZero():
   fo = open(fileName, "w")
   fo.write(defaultStr)
   fo.close()
   
def getup(v=0):
   fo = open(".uspw", "r")
   line1 = fo.readline()
   line2 = fo.readline()
   fo.close()
   if v == 0:
      return line1[:-1]
   else:
      return line2[:-1]
