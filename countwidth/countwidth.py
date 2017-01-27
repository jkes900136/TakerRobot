from Tkinter import *
import serial
import tkMessageBox
from time import sleep
import bluetooth
import numpy as np
import cv2
import imutils
import time
from SimpleCV import Camera

 


def ShippingAndReserved(self,camera):
            time.sleep(3)  # If you don't wait, the image will be dark
            return_value, image = camera.read()
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (5, 5), 0)
            thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.erode(thresh, None, iterations=2)
            thresh = cv2.dilate(thresh, None, iterations=2)
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0]
            while(True):
                try:
                    c = max(cnts, key=cv2.contourArea)
                    break;
                except:
                    time.sleep(5)
            extLeft = tuple(c[c[:, :, 0].argmin()][0])
            extRight = tuple(c[c[:, :, 0].argmax()][0])
            extTop = tuple(c[c[:, :, 1].argmin()][0])
            extBot = tuple(c[c[:, :, 1].argmax()][0])
            ##mm = list(c[c[:, :, 0].argmax()][0])
           ## nn = list(c[c[:, :, 0].argmin()][0])
            ttt = str (list(c[c[:, :, 0].argmax()][0]-(c[c[:, :, 0].argmin()][0])))#the right side point x - left side point x value
            ppp = int(ttt[1]+ttt[2]+ttt[3])
            if ppp<100:
              kk = int(ttt[1]+ttt[2])
              global tt
              tt = kk/41
              if tt>10:
                tt=9
              elif tt<2:
                tt=4
            else:
              tt = ppp/41
              if tt>10:
                tt=9
              elif tt<2:
                tt=4
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
