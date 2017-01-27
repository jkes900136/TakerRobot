import cv2
import numpy as np
import time



def cam(cap):

    _, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)




    lower_blue = np.array([110,50,50])
    upper_blue = np.array([130,255,255])
    lower_green = np.array([50,100,100])
    upper_green = np.array([70,255,255])
    lower_red = np.array([-10,100,100])
    upper_red = np.array([10,255,255])
    lower_orange = np.array([11,43,46])
    upper_orange = np.array([19,255,255])
    lower_yellow = np.array([20,100,100])
    upper_yellow = np.array([30,255,255])
    #######
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_red = cv2.inRange(hsv, lower_red, upper_red)
    mask_green = cv2.inRange(hsv, lower_green, upper_green)
    mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
    mask_yellow = cv2.inRange(hsv, lower_yellow, upper_yellow)
    #######
    count_blue = mask_blue.sum()
    count_red = mask_red.sum()
    count_green = mask_green.sum()
    count_orange = mask_orange.sum()
    count_yellow = mask_yellow.sum()  

    countcolor=[count_blue,count_red,count_green,count_orange,count_yellow]
    return countcolor
