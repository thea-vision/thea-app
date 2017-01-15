import numpy as np
from matplotlib import pyplot as plt
import cv2
import copy
from os import listdir
from os.path import isfile, join
from mlab.releases import R2012b as mlab
from matlab import matlabroot
import math

print matlabroot()

class Object(object):
    pass

mlab.addpath('C:\Users\Kent\Documents\MATLAB\Daugman')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
imageSourcePath = "imageSource"
imageOutputPath = "imageOutputs"
imageSources = [f for f in listdir(imageSourcePath) if isfile(join(imageSourcePath, f))]

params = Object()
#gaussianParams
params.gKernelX = 3
params.gKernelY = 3
params.sigmaX = 0
#threshParams
params.tThresh = 100
params.tMaxVal = 255
params.tType = cv2.THRESH_BINARY_INV
#cannyParams
params.cMinVal = 100
params.cMaxVal = 50
#houghParams
params.hResolutionScale = 1
params.hMinCircDist = 100
params.hAccum = 15 #Higher means less circles detected
params.hMinRadius = 5
#growingCircleParams
params.gcIters = 1
#lightThreshParams
params.ltThresh = 200
params.ltMaxVal = 255
params.ltType = cv2.THRESH_BINARY
#lightCannyParams
params.lcMinVal = 100
params.lcMaxVal = 50
#lightHoughParams
params.lhResolutionScale = 1
params.lhMinCircDist = 1000
params.lhAccum = 3 #Higher means less circles detected
#lightGaussianParams
params.glKernelX = 5
params.glKernelY = 5
params.glSigmaX = 0



for imageSource in imageSources:
    print imageSource
    img = cv2.imread(join(imageSourcePath, imageSource))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    eyes = eye_cascade.detectMultiScale(gray)
    length = len(eyes)
    eyeCollection = []
    eyeNum = 0
    eyeCenter = []
    for (ex,ey,ew,eh) in eyes:
        eyeNum = eyeNum + 1
        cv2.rectangle(img,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
        eye = img[ey:ey+eh, ex:ex+ew];

        grayeye = cv2.GaussianBlur(cv2.cvtColor(eye, cv2.COLOR_BGR2GRAY),(params.gKernelX,params.gKernelY),params.sigmaX)
        ret, thresh1 = cv2.threshold(grayeye,params.tThresh,params.tMaxVal,params.tType)
        canny = cv2.Canny(thresh1, params.cMinVal, params.cMaxVal)

        try:
            cv2.imwrite(join(imageOutputPath, imageSource) + str(eyeNum) + ".jpg", grayeye)

            mlab.thresh(join(imageOutputPath, imageSource) + str(eyeNum) + ".jpg", 30, 100);
            with open(join(imageOutputPath, imageSource) +str(eyeNum)+ ".jpgi") as csvfile:
                circParam = csvfile.readline().split(',')
                circParam = map(int, circParam)
                cv2.circle(eye,(circParam[1],circParam[0]),circParam[2],(255,0,0),1)
                cv2.circle(eye,(circParam[1],circParam[0]),1,(0,0,0),1)

                #troubleshoot
                #plt.imshow(grayeye)
                #plt.show()

                lightReflexEyeO = grayeye[circParam[0] - circParam[2]:circParam[0]+circParam[2], circParam[1] - circParam[2]:circParam[1]+circParam[2]]

                #troubleshoot
                #plt.imshow(lightReflexEyeO)
                #plt.show()

                lightReflexEye = cv2.GaussianBlur(lightReflexEyeO,(params.glKernelX,params.glKernelY),params.glSigmaX)
                ret, threshLight = cv2.threshold(lightReflexEye,params.ltThresh,params.ltMaxVal,params.ltType)
                cannyLight = cv2.Canny(threshLight, params.lcMinVal, params.lcMaxVal)

                #troubleshoot
                #plt.imshow(threshLight)
                #plt.show()

                circles = cv2.HoughCircles(threshLight,cv2.cv.CV_HOUGH_GRADIENT,params.lhResolutionScale,params.lhMinCircDist, param1=params.lcMinVal, param2=params.lhAccum, minRadius=1)
                circles = np.uint16(np.around(circles))

                for j in circles[0,:]:
                    cv2.circle(lightReflexEyeO,(j[0],j[1]),1,(0,0,0),1)
                    cv2.circle(eye,(circParam[1] - circParam[2] + j[0], circParam[0] - circParam[2] + j[1]),1,(0,0,0),1)
                    print 'Light reflex parameters: ' + str(circParam[1] - circParam[2] + j[0]) + ' ' + str(circParam[0] - circParam[2] + j[1])

                #troubleshoot
                #plt.imshow(lightReflexEyeO)
                #plt.show()
                print 'Iris parameters: ' + str(circParam[1]) + ' ' + str(circParam[0]) + ' '  + str(circParam[2])
                print 'Distance: ' + str(((circParam[1]- (circParam[1] - circParam[2] + j[0]))**2 + (circParam[0] - (circParam[0] - circParam[2] + j[1]))^2)**0.5)
                print 'Angle: ' + str(math.atan2((circParam[0] - (circParam[0] - circParam[2] + j[1])),(circParam[1]- (circParam[1] - circParam[2] + j[0]))) * 180 / 3.14)
                plt.imshow(grayeye)
                plt.show()
                cv2.imwrite(join(imageOutputPath, imageSource) + str(eyeNum) + ".jpg", img)


        except Exception as e:
            print e
