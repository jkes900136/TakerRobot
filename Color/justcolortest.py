import cv2
import numpy as np
import time
import scancolor
cap = cv2.VideoCapture(0)
blue_threshold = 22222222
red_threshold = 22222222
green_threshold = 22222222
orange_threshold =22222222
yellow_threshold =18000000
# This value you could change for what works best

while True:
    
    countcolor = scancolor.cam(cap)
    _, frame = cap.read()
    if countcolor[0] > blue_threshold:
       print 'blue'
    elif countcolor[1] > red_threshold:
       print 'red'
    elif countcolor[2] > green_threshold:
       print 'green'
    elif countcolor[3] > orange_threshold:
       print 'orange'
    elif countcolor[4] > yellow_threshold:
       print 'yellow'
##    else :
##        print ' no color'

    cv2.imshow('Colorframe',frame)
    #cv2.imshow('mask',mask)
    #cv2.imshow('mask_blue)',mask_blue)
    #cv2.imshow('mask_green',mask_green)
    #cv2.imshow('mask_red',mask_red)
    #cv2.imshow('mask_orange',mask_orange)
    #cv2.imshow('mask_yellow',mask_yellow)


    #time.sleep(0.8)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cv2.destroyAllWindows()
