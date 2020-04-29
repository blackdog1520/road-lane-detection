import cv2
import os
import numpy as np

def cannyImage(sampleImage):
    gray = cv2.cvtColor(sampleImage,cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray,(15,15),0)
    canny = cv2.Canny(blur,50,150)
    return canny

def averagedLines(image,lines):
    left_fit = []
    right_fit= []
    if lines is not None:
        
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            parameters = np.polyfit((x1,x2),(y1,y2),1)     #this parameters contain slope of line and y intercept of the line
            slope = parameters[0]
            Yintercept = parameters[1]
            if slope<=0:
                left_fit.append(parameters)
            else:
                right_fit.append(parameters)
        left_fit_average = np.average(left_fit,axis = 0)
        right_fit_average = np.average(right_fit,axis = 0)
        left_line = coordinates(image,left_fit_average)
        right_line = coordinates(image,right_fit_average)
        return np.array([left_line,right_line])
    else:
        return None
        

def coordinates(image,average):
    try:
        slope, intercept = average
    except TypeError:
        slope, intercept = 0.1, 0
    y1 = image.shape[0]
    y2 = int(y1*2/4)
    x1 = int((y1-intercept)/slope)
    x2 = int((y2-intercept)/slope)
    return np.array([x1,y1,x2,y2])
    
   
def regionOfInterest(testimage):
    imageHeight = testimage.shape[0]
    poly = np.array([[(0,imageHeight-240),(1200,imageHeight),(800,400)]])       #this polygon is to detect the ends of lane we are travelling on set the coordinates according to plot using matplotlib the starting point of lanes and the ending points of lane to form a triangle
    blackMask = np.zeros_like(testimage)
    cv2.fillPoly(blackMask,poly,255)
    finalRegion = cv2.bitwise_and(blackMask,testimage)
    poly2 = np.array([[(20,imageHeight-200),(1150,imageHeight),(800,300)]])     #this polygon we are drawing beacuse to avoid the signs that are on the road
    blackMask2 = np.ones_like(testimage)
    cv2.fillPoly(blackMask2,poly2,0)
    newfinalRegion = cv2.bitwise_and(blackMask2,finalRegion)
    
    return newfinalRegion


def dispLane(Image,lines):
    line_image = np.zeros_like(Image)
    line_image_gray = cv2.cvtColor(line_image,cv2.COLOR_GRAY2RGB)
    if lines is not None:
        for x1,y1,x2,y2 in lines:
            cv2.line(line_image_gray,(x1,y1),(x2,y2),(0,255,0),10)
    return line_image_gray

#image = cv2.imread('test.png')
#laneImage = np.copy(image)
##laneImage = cv2.resize(image,(1000,1000))
##newGray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
#cannyImage = cannyImage(laneImage)
#interestImage = regionOfInterest(cannyImage)    #we get the region of interest that is the traingle which is formed by two lanes and cars origin
#linesForLane = cv2.HoughLinesP(interestImage,2,np.pi/180,100,np.array([]),minLineLength = 10,maxLineGap = 5)
#averagedLinesLane = averagedLines(interestImage,linesForLane)
#imageWithLine = dispLane(interestImage,averagedLinesLane)
#combinedImage = cv2.addWeighted(image , 0.8 , imageWithLine , 1 , 1)
##averagedLines(interestImage,linesForLane)
#
#cv2.imshow("lane detection",combinedImage)
#cv2.waitKey(0)

camera = cv2.VideoCapture('newTestVidio.mp4')

while(camera.isOpened()):
    ret,frame = camera.read()
    laneImage = np.copy(frame)
    cannyimage = cannyImage(laneImage)
    interestImage = regionOfInterest(cannyimage)    #we get the region of interest that is the traingle which is formed by two lanes and cars origin
    linesForLane = cv2.HoughLinesP(interestImage,2,np.pi/180,100,np.array([]),minLineLength = 10,maxLineGap = 30)
    averagedLinesLane = averagedLines(interestImage,linesForLane)
    if averagedLinesLane is None:
        averagedLinesLane = averaged
    else:
        averaged = averagedLinesLane
    imageWithLine = dispLane(interestImage,averagedLinesLane)
    combinedImage = cv2.addWeighted(laneImage , 0.8 , imageWithLine , 1 , 1)
    cv2.imshow("lane detection", combinedImage)
    cv2.waitKey(10)



