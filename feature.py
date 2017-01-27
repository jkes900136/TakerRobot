from Tkinter import *
import serial
import tkMessageBox
from time import sleep
import bluetooth
import numpy as np
import cv2

def featureee(camera):
            orb = cv2.ORB()
            bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

            imgTrainColor=cv2.imread('arrow3.jpg')
            imgTrainGray = cv2.cvtColor(imgTrainColor, cv2.COLOR_BGR2GRAY)

            kpTrain = orb.detect(imgTrainGray,None)
            kpTrain, desTrain = orb.compute(imgTrainGray, kpTrain)

            firsttime=True
            while True:
              try:
                    ret, imgCamColor = camera.read()
                    imgCamGray = cv2.cvtColor(imgCamColor, cv2.COLOR_BGR2GRAY)
                    kpCam = orb.detect(imgCamGray,None)
                    kpCam, desCam = orb.compute(imgCamGray, kpCam)
                    matches = bf.match(desCam,desTrain)
                    dist = [m.distance for m in matches]
                    thres_dist = (sum(dist) / len(dist)) * 0.5
                    matches = [m for m in matches if m.distance < thres_dist]
                    break
              except:
                        continue     
            if firsttime==True:
                #print'55454'
                h1, w1 = imgCamColor.shape[:2]
                h2, w2 = imgTrainColor.shape[:2]
                nWidth = w1+w2
                nHeight = max(h1, h2)
                hdif = (h1-h2)/2
                firsttime=False
            result = np.zeros((nHeight, nWidth, 3), np.uint8)
            result[:h1, w2:w1+w2] = imgCamColor
            result[hdif:hdif+h2, :w2] = imgTrainColor
            pt_bx=0
            pt_by=0
            for i in range(len(matches)):
                pt_a=(int(kpTrain[matches[i].trainIdx].pt[0]), int(kpTrain[matches[i].trainIdx].pt[1]+hdif))
                pt_b=(int(kpCam[matches[i].queryIdx].pt[0]+w2), int(kpCam[matches[i].queryIdx].pt[1]))
                cv2.line(result, pt_a, pt_b, (255, 0, 0))
                pt_bx+=int(kpCam[matches[i].queryIdx].pt[0]+w2)
                pt_by+=int(kpCam[matches[i].queryIdx].pt[1])
            countfeature=[len(matches),pt_bx,pt_by,w2,result]
            return countfeature
