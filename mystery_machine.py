import serial
import sys
import cv2 as cv
from image_analysis import getTestImages, getArenaObstaclesMatrix, getGoalPosition, getRobotPosition
from potential_fields import getPathMatrix
from robot_action import moveRobot
from time import sleep, time

#Serial
arduino = serial.Serial("COM5", 9600)
sleep(2)

def TestParams():

    original, warped, tresh, obstacles, maskBlue, maskGreen, maskRed = getTestImages()

    winname = "Original"
    cv.namedWindow(winname)     
    cv.moveWindow(winname, 40,30) 
    cv.imshow(winname, original)

    winname = "Warped"
    cv.namedWindow(winname)     
    cv.moveWindow(winname, 250,30) 
    cv.imshow(winname, warped)

    winname = "Tresh"
    cv.namedWindow(winname)     
    cv.moveWindow(winname, 460,30) 
    cv.imshow(winname, tresh)

    winname = "Obstacles"
    cv.namedWindow(winname)     
    cv.moveWindow(winname, 670,30) 
    cv.imshow(winname, obstacles)

    winname = "Blue"
    cv.namedWindow(winname)     
    cv.moveWindow(winname, 880,30) 
    cv.imshow(winname, maskBlue)

    winname = "Green"
    cv.namedWindow(winname)     
    cv.moveWindow(winname, 1090,30) 
    cv.imshow(winname, maskGreen)

    winname = "Red"
    cv.namedWindow(winname)     
    cv.moveWindow(winname, 1300,30) 
    cv.imshow(winname, maskRed)


#Test Params
TestParams()

k = cv.waitKey()
if k%256 == 27:
    # Configuration needs changes
    sys.exit(0)


# Main Logic
_, obstaclesMatrix = getArenaObstaclesMatrix()
goalPosition = getGoalPosition()
HPF = getPathMatrix(obstaclesMatrix, goalPosition, 2000)

corgi = cv.imread('photos/corgi_motivacional.jpg')
cv.imshow('Enter para continuar', corgi)
cv.waitKey()

arduino.write(b'9')
while(True):
    position, robotAngle = getRobotPosition()
    moveRobot(HPF, position, robotAngle, arduino)
    # sleep(0.005)