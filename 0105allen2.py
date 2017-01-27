from Tkinter import *
##Built-in
import serial
##    sudo apt-get install python-serial
import tkMessageBox
##Built-in ， It comes with Tkinter
from time import sleep
##Built-in
import bluetooth
##sudo apt-get install pi-bluetooth
import numpy as np
##sudo apt-get install python-numpy python-scipy python-matplotlib ipython
import cv2
##sudo apt-get install libopencv-dev python-opencv 
import cv2.cv as cv
##sudo apt-get install libopencv-dev python-opencv
import zbar
##sudo apt-get install python-zbar
import datetime
##Built-in
import time
##Built-in
import threading
###Built-in
import imutils
##sudo pip install imutils
from SimpleCV import Camera
##1.sudo apt-get install ipython python-opencv python-scipy python-numpy python-pygame python-setuptools python-pip
##2.sudo pip install https://github.com/sightmachine/SimpleCV/zipball/develop
##sudo pip install svgwrite
import sys
##Built-in
import os
##Built-in
import webcatcher1019
import scancolor
import countwidth
import feature

chkwork="reserved"
wloop=1
wchecker=0
mainwork=0
placeid="rodname="
shelfid=""
row=""
col=""
turnfromweb=""
cama=1
camb=0
listindex=0
countlist=0
backturn=[]
countRL=[]
turn2=False
qronce=0
#bd_addr="00:0D:19:03:19:FA"
bd_addr="00:0D:19:0E:14:E6"
#bd_addr="00:0D:19:03:19:FA"
port = 1
sock=bluetooth.BluetoothSocket(bluetooth.RFCOMM)

def connect():
    while(True):    
        try:
            gaugeSocket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
            gaugeSocket.connect((bd_addr, port))
            break;
        except bluetooth.btcommon.BluetoothError as error:
            gaugeSocket.close()
            print "Could not connect: ", error, "; Retrying in 5s..."
            time.sleep(5)
    return gaugeSocket;

sock = connect()


class CarMove():

   def _init_(self):
      pass
   def move(self,data1,data2,data3):
      CarTXD=chr(0x80)+chr(0x7f)+chr(data1)+chr(data2)+chr(0x0f)+\
                chr(data3)+chr(0x00)+chr(0x80)
      sock.send(CarTXD)
      #print 1111

class ArmMove():

    def _init_(self):
        pass
    def move(self,data):
      ArmTXD=chr(0xff)+chr(0xff)+chr(0x01)+chr(data)+chr(0xff)+chr(0xff)+chr(0xff)
      sock.send(ArmTXD)



speed=35
car=CarMove()
arm=ArmMove()


#### the follwing is scaning qrcode
class BarCodeScanner( Frame,threading.Thread ):
############################################################################
   
   def __init__(self, mainwork, chkwork, ssn, iname, shelf,row,col):
        threading.Thread.__init__(self)
   def scan(self, frame):
        global qronce,shelfid,shelfidRL
        
       # print shelfidRL
        imgray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        raw = str(imgray.data)

        scanner = zbar.ImageScanner()
        scanner.parse_config('enable')          
       
        width = int(self.cap.get(cv.CV_CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv.CV_CAP_PROP_FRAME_HEIGHT))
        imageZbar = zbar.Image(width, height,'Y800', raw)
        scanner.scan(imageZbar)
                
        for symbol in imageZbar:
            cv2.putText(frame, 'decoded' +str(symbol.type)+ 'symbol'+ '"%s"' % str(symbol.data),(frame.shape[1] -1375,frame.shape[0] -3),cv2.FONT_HERSHEY_SIMPLEX,
                        2.0,(0,255,0),3)
            print 'decoded', symbol.type, 'symbol', '"%s"' % symbol.data
            global turn2
            global test,seered
            turn2=True
            if qronce == 0:  
              if "%s" % symbol.data == shelfid:
                 qronce=qronce+1
                 self.RightShelfAndChangeImage()
                 if shelfidRL%2==0:
                   print "double"
                   car.move(speed,0,99)
                   time.sleep(5)
                   seered=True
                 elif shelfidRL%2==1:
                   print"single"  
                   car.move(speed,0,101)
                   time.sleep(5)
                   seered=True
##              elif "%s" % symbol.data == "a2":
##                  pass
              elif "%s" % symbol.data == "bottle":   
               print "This is a bottle"
               test=True
              elif "%s" % symbol.data == "box":   
               print "This is a box"
               test=True
              elif "%s" % symbol.data == "paperball":   
               print "This is a paperball"
               test=True
              elif "%s" % symbol.data == "papercup":   
               print "This is a papercup"
               test=True
              elif "%s" % symbol.data == "Right":   
               print "Too Right"
               global tooright
               qronce=qronce+1
               tooright=True
              elif "%s" % symbol.data == "left":   
               print "Too Left"
               global tooleft
               qronce=qronce+1
               tooleft=True 
              else:   
               print "inothershelf"
               seered=True
               pass
##               global wrong
##               wrong = True
   def ShippingAndReserved(self,tt):
                
#####
                print tt
                time.sleep(5)
                car.move(128,127,0)
                time.sleep(1.5)
                if chkwork=="reserved":
                    arm.move(21)
                    time.sleep(3)
                    arm.move(tt-1)
                    time.sleep(5)
                    arm.move(tt+8)
                    time.sleep(3)
                    print 'taking thing reserved'
#####
                elif chkwork=="shipping":
                    arm.move(20)
                    time.sleep(8)
                    arm.move(tt-1)
                    time.sleep(5)
                    car.move(speed,0,43)
                    time.sleep(1.5)
                    car.move(speed,0,99)
                    time.sleep(8)
                    arm.move(tt+8)
                    time.sleep(3)
                    print 'taking thing shipping'
#####
   def End(self):
      car.move(128,127,0)#######The End
      time.sleep(2)
      print 'haha'
      car.move(0,0,50)
      print 'hoho'
      time.sleep(14)
      arm.move(tt)
      time.sleep(2)
      arm.move(21)
      time.sleep(2)
      car.move(speed,0,43)
      time.sleep(4)
      car.move(speed,0,63)
      time.sleep(8)
   def InGreen(self,camera,cap):
      global row
      y=int(row)
      print y
      print "in seegreen"
      car.move(128,127,0)
      time.sleep(1.5)
      if y == 1:
            car.move(0,0,50)
            time.sleep(35)
            print "y=1"
      elif y == 2:
            car.move(0,0,51)
            time.sleep(25)
            print "y=2"
      elif y == 3:
            car.move(0,0,53)
            time.sleep(15)
            print "y=3"
      if chkwork=="reserved":
            car.move(speed,0,14)
            time.sleep(2)
            arm.move(21)
            time.sleep(4)
            car.move(speed,0,43)
            time.sleep(2)
            car.move(speed,0,99)
            time.sleep(8)
      elif chkwork=="shipping":
            car.move(speed,0,16)
            time.sleep(2)
            global qronce
            qronce=0
            self.cap.release()
            camera.release()
            time.sleep(1)
            self.cap = cv2.VideoCapture(cama)
            camera = cv2.VideoCapture(camb)
   def TooRightOrLeft(self,camera,cap):
      if   tooright == True:
       car.move(speed,0,18)
      elif tooleft == True:
       car.move(speed,0,20)
      self.cap.release()
      camera.release()
      time.sleep(1)
      self.cap = cv2.VideoCapture(cama)
      camera = cv2.VideoCapture(camb)
      tooright = False
   def Down(self,camera,cap):
      self.cap.release()
      camera.release()
      time.sleep(1)
      self.cap = cv2.VideoCapture(cama)
      camera = cv2.VideoCapture(camb)
   def HaveCornerOrNot(self):
      global countRL,turnfromweb,imgTrainColor,shelfidRL,shelfid,shelfidlist
      shelfidlist=[]
      for a in shelfid:
          shelfidlist = shelfidlist+[a]
      shelfidRL=int(shelfidlist[1])
      print shelfidRL
      for q in turnfromweb:
          countRL = countRL+[q]
          if countRL==["N"]:
              if shelfidRL%4==1:
                  imgTrainColor=cv2.imread('shelf.jpg')
                  print "shelfid%4==1"
              elif shelfidRL%4==2:
                  imgTrainColor=cv2.imread('shelf.jpg')
                  print "shelfid%4==2"
              elif shelfidRL%4==3:
                  imgTrainColor=cv2.imread('shelf.jpg')
                  print "shelfid%4==3"
              elif shelfidRL%4==0:
                  imgTrainColor=cv2.imread('shelf.jpg')
                  print "shelfid%4==0"
              
          else:    
              imgTrainColor=cv2.imread('arrow3.jpg')
              print "she"
   def RightShelfAndChangeImage(self):
      global  imgTrainColor,shelfidRL,orb,kpTrain
      if shelfidRL%4==1:
          imgTrainColor=cv2.imread('shelf.jpg')
          print "shelfid%4==1"
      elif shelfidRL%4==2:
          imgTrainColor=cv2.imread('shelf.jpg')
          print "shelfid%4==2"
      elif shelfidRL%4==3:
          imgTrainColor=cv2.imread('shelf.jpg')
          print "shelfid%4==3"
      elif shelfidRL%4==0:
          imgTrainColor=cv2.imread('shelf.jpg')
          print "shelfid%4==0"
      imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)
      kpTrain = orb.detect(imgTrainGray,None)
      kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)    
   def TurnRightOrTurnLeft(self,back):
      global listindex,countlist,backturn,countRL,turnfromweb
      for q in turnfromweb:
         countRL = countRL+[q]
         countlist+=1
      if back == True:
             print'bture'
             while listindex<=countlist:
                 if backturn[listindex-1] =="R":
                     print backturn[listindex-1]
                     car.move(128,127,0)
                     time.sleep(2)
                     car.move(speed,0,101)
                     time.sleep(5)
                     print listindex
                     print '~~~R~~~'
                     listindex-=1
                     break
                 elif backturn[listindex-1]=="L":
                     car.move(128,127,0)
                     time.sleep(2)
                     car.move(speed,0,99)
                     time.sleep(5)
                     print listindex
                     print '~~~L~~~'
                     listindex-=1
                     break
      else:
             print 'else'
             while listindex<=countlist:
                 print listindex
                 if countRL[listindex]=="R":
                     print countRL[listindex]
                     car.move(128,127,0)
                     time.sleep(2)
                     car.move(speed,0,101)
                     time.sleep(5)
                     print listindex
                     print '~~~R~~~2'
                     listindex+=1
                     backturn+=["L"]
                     break
                 elif countRL[listindex]=="L":
                     car.move(128,127,0)
                     time.sleep(2)
                     car.move(speed,0,99)
                     time.sleep(5)
                     print listindex
                     print '~~~L~~~2'
                     listindex+=1
                     backturn+=["R"]
                     break
                 else:
                     pass     
############################################################################
   def run(self):
      global mainwork
      global placeid
      global prodname
      global shelfid
      global row
      global col
      global turnfromweb,seered,shelfidRL
      turncount=0
      seered=False
      global test
      test=False
      closecam=0
      cr=0
      cl=0
      global back,qronce
      back = False
      backandstop= False
      End = False
      seegreen = False
      seegreen2=False
      global wrong
      wrong = False
      global tooright
      tooright = False
      global tooleft
      tooleft = False
      reserved=''
      if chkwork=="reserved":#What task will be doing at this segment
         editwork="occupied"
         reserved='down'
      elif chkwork=="shipping":
         editwork="empty"
      print editwork,
      print chkwork,
      print placeid,
      print prodname,
      print shelfid,
      print row,
      print col,
      arm.move(1)
      time.sleep(2)
      car.move(0,0,55)
      
      
      #time.sleep(45)
#######
      global imgTrainColor,orb,kpTrain,imgTrainGray
      orb = cv2.ORB()
      bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
##      imgTrainColor=cv2.imread('arrow3.jpg')
##      imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)
##      kpTrain = orb.detect(imgTrainGray,None)
##      kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)
      global firsttime
      firsttime=True
      
      self.HaveCornerOrNot()
      imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)
      kpTrain = orb.detect(imgTrainGray,None)
      kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)
      while True:
          
          if (reserved=='' or reserved=='down')and seered==False:
              camera = cv2.VideoCapture(cama)
              self.cap = cv2.VideoCapture(camb)
              print "1"
          else:
              self.cap.release()
              camera.release()
              time.sleep(5)
              camera = cv2.VideoCapture(cama)
              self.cap = cv2.VideoCapture(camb)
              seered=False
              print "2"
          if wrong ==True:
              print 'OPPS wrong-End'
              break
          print'GOGOGO'
          while True:
            try:
                    global sock
                    stoptext=sock.recv(1024)                    
                    print stoptext
                    if stoptext.isdigit() == False:
                     ##print "dsadasdasdasdasdasdasdasdadasdasdasdasdasdas"
                       webcatcher1019.extract("http://isla.shu.edu.tw:8066/gt2016/TakerRobot/auditingedit.php?action=error&accid=Robot2")
                    else:
                       webcatcher1019.extract("http://isla.shu.edu.tw:8066/gt2016/TakerRobot/auditingedit.php?action=working&accid=Robot2")
            except bluetooth.btcommon.BluetoothError as error:
                    print "Caught BluetoothError: ", error
                    time.sleep(5)
                    sock = connect()
                    pass
            #######
            blue_threshold = 22222222
            red_threshold = 22222222
            green_threshold = 22222222
            orange_threshold =22222222
            yellow_threshold =18000000    
            countcolor = scancolor.cam(self.cap)
            
            ##color
#######    
#######        
            if countcolor[0] > blue_threshold:
               print 'blue'
               if ctype != 'b':
                   self.TurnRightOrTurnLeft(back)
                   ctype='b'
            elif countcolor[1] > red_threshold:
               print 'red'
               car.move(128,127,0)
               time.sleep(2)
               car.move(speed,0,14)
               time.sleep(2)
               global qronce
               qronce=0
               ctype='r'
               break
            elif countcolor[2] > green_threshold:
               print 'green'
               if ctype != 'g':
                   car.move(128,127,0)
                   back=True
                   ctype='g'
                   closecam=closecam+1
                   seegreen=True
                   seegreen2=True
##
##            elif countcolor[3] > orange_threshold:
##               print 'orange'
##               if ctype != 'o':
##                   closecam=closecam+1  
##                   car.move(128,127,0)  
##                   time.sleep(2)
##                   car.move(speed,0,101)
##                   time.sleep(3)
##                   car.move(speed,0,41)
##                   ctype='o'
            else:
                closecam=0
                ctype=''
################## robot green action
            if test ==True and backandstop==False:
               print"confirm"
               tt = countwidth.ShippingAndReserved(camera)
               self.ShippingAndReserved(tt)
               test=False
               seegreen2=False
               if chkwork=="shipping":
                  backandstop=True
##################  robot green action END                  
            elif reserved == 'down':
               reserved = ''
               self.Down(camera,self.cap)
               break
            elif tooright == True or tooleft == True:
               self.TooRightOrLeft(camera,self.cap)
               qronce=0
               break
            elif seegreen2== True and backandstop==True:
               self.End()
               End = True
               break
            elif seegreen == True and backandstop==False:
               self.InGreen(camera,self.cap)
               if chkwork=="reserved":
                    seegreen2= False
                    backandstop = True 
               elif chkwork=="shipping":
                    break
##################robot green action end
            countfeature=feature.featureee(camera)
            if countfeature[0]>1 and closecam==0:
                        countfeature[1]=(countfeature[1]/countfeature[0])-countfeature[3]
                        countfeature[2]=countfeature[2]/countfeature[0]
                        if countfeature[1] < 220 :
                                cv2.putText(countfeature[4], "left" ,
                                (countfeature[4].shape[1] - 800, countfeature[4].shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                                2.0,    (0, 255, 0), 3)
                                
                                if countfeature[1] < 210 :
                                  
                                     car.move(speed,0,65)      
                                     ret, imgCamColor = camera.read()
                                     time.sleep(2)
                                else:
                                   
                                     car.move(speed,0,69)
                                     ret, imgCamColor = camera.read()
                                     time.sleep(2)
                                  
                        elif countfeature[1] > 345: 
                                cv2.putText(countfeature[4], "right" ,
                                (countfeature[4].shape[1] - 800, countfeature[4].shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                                2.0, (0, 255, 0), 3)
                                if countfeature[1] > 350:
                                  car.move(speed,0,71)
                                  ret, imgCamColor = camera.read()
                                  time.sleep(2)
                                else:
                                  car.move(speed,0,67)
                                  ret, imgCamColor = camera.read()
                                  time.sleep(2)
                        else:
                                cv2.putText(countfeature[4], "middle" ,
                                (countfeature[4].shape[1] - 800, countfeature[4].shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                                2.0, (0, 255, 0), 3)
                                car.move(speed,0,41)
                        cv2.putText(countfeature[4], ctype+"-"+str(countfeature[1])+","+str(countfeature[3]),
                                (countfeature[4].shape[1] - 400, countfeature[4].shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                                2.0, (0, 255, 0), 3)   
            else :
                        cv2.putText(countfeature[4], "Not found" ,(countfeature[4].shape[1] - 800, countfeature[4].shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX,
                        2.0, (0, 255, 0), 3)
                        car.move(speed,0,41)
            cv2.imshow('Camara', countfeature[4])    
            k = cv2.waitKey(5) & 0xFF    
            
                   
            
       

          cv2.destroyAllWindows()
          self.WINDOW_NAME = 'Qrcode'
          self.CV_SYSTEM_CACHE_CNT = 5 # Cv has 5-frame cache
          self.LOOP_INTERVAL_TIME = 0.2
          cv.NamedWindow(self.WINDOW_NAME, cv.CV_WINDOW_NORMAL)
          global turn2
          if End==True:
               webcatcher1019.extract("http://isla.shu.edu.tw:8066/gt2016/TakerRobot/nShop/Prodplaceedit.php?action={0}&placeid={1}".format(editwork,placeid))
               webcatcher1019.extract("http://isla.shu.edu.tw:8066/gt2016/TakerRobot/auditingedit.php?action=working&accid=Robot2")        
               print 'end'
               mainwork=0             
               
               break
          while True:
                         
                if turn2==True:
                    
                    turn2=False
                    self.cap.release()
                    cv2.destroyAllWindows()
                    break
                    
                for i in range(0,self.CV_SYSTEM_CACHE_CNT):
                   #print 'Read2Throw', time.time()
                    self.cap.read()
                #print 'Read2Use', time.time()
                img = self.cap.read()
                self.scan(img[1])

                cv2.imshow(self.WINDOW_NAME, img[1])
                cv.WaitKey(1)
                #print 'Sleep', time.time()
                time.sleep(self.LOOP_INTERVAL_TIME)

while(wloop):
    links=[]
    linkscount=0
    placeid=""
    prodname=""
    shelfid=""
    row=""
    col=""
    if chkwork=="reserved":
        chkwork="shipping"
        print  chkwork
    elif chkwork=="shipping":
        chkwork="reserved"
        print   chkwork
    links=webcatcher1019.extract("http://isla.shu.edu.tw:8066/gt2016/TakerRobot/nShop/listforbot.php?action={0}".format(chkwork))
    webcatcher1019.extract("http://isla.shu.edu.tw:8066/gt2016/TakerRobot/auditingedit.php?action=working&accid=Robot2")
    for l in links:
            print(l),
            if linkscount>0 and linkscount<=9:
                if linkscount==2:
                    placeid=l
                if linkscount==3:
                    prodname=l
                if linkscount==4:
                    shelfid=l
                if linkscount==5:
                    row=l
                if linkscount==6:
                    col=l
                if linkscount==7:
                    turnfromweb=l
            if l !='0':
                #print 'start',
                wchecker=1
                linkscount+=1
    time.sleep(1)
    if(wchecker):
        wchecker=0
        mainwork=1
        #wloop=0
        scanner = BarCodeScanner(wchecker,chkwork,placeid, prodname, shelfid,row,col)
        scanner.start()
        while(mainwork==1):
            #print "waiting"
            time.sleep(1)
    else:
         print ''

                

      


