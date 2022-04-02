import cv2 as cv
import numpy as np
import math

#Camera
cam = cv.VideoCapture(2)

# COLORS THRESHOLDS 
lower_red = np.array([0,0,200])       # Red
upper_red = np.array([140,140,255])     # Red
lower_green = np.array([80,120,0])     # Green
upper_green = np.array([160,220,40])   # Green
lower_blue = np.array([105,0,0])      # Blue
upper_blue = np.array([200,100,90])  # Blue
lower_black = 70                     # Black
upper_black = 255                     # Black

# Cleaning values
kernel = np.ones((3,3),np.uint8)

# Arena
arena_limits = [[64, 94], [564, 89], [7, 375], [634, 363]]
arena_size = (187,100)  #Tambien esta en campos potenciales
error_expansion = 9 #cm

# Image
image_width = 640
image_height = 480



#        Analysis       #
def getImage():
    # Reading and Resizing image
    _, frame = cam.read()
    _, frame = cam.read()
    pts1 = np.float32(arena_limits)
    pts2 = np.float32([[0, 0], [image_width, 0], [0, image_height], [image_width, image_height]])
    matrix = cv.getPerspectiveTransform(pts1, pts2)
    warped = cv.warpPerspective(frame, matrix, (image_width, image_height))
    warped = cv.resize(warped,arena_size,interpolation=cv.INTER_AREA)

    return warped

def getTestImages():
    _, frame = cam.read()
    _, frame = cam.read()
    original =  cv.resize(frame,arena_size,interpolation=cv.INTER_LINEAR)
    warped = getImage()
    tresh, obstacles = getArenaObstaclesMatrix()
    maskBlue = cv.inRange(warped, lower_blue, upper_blue)
    maskGreen = cv.inRange(warped, lower_green, upper_green)  
    maskRed = cv.inRange(warped, lower_red, upper_red) 

    cv.imwrite('savedImage.jpg',warped)


    return original, warped, tresh, obstacles, maskBlue, maskGreen, maskRed

def getArenaObstaclesMatrix():
    image = getImage()
    width, height = getHalf(arena_size[0]) , getHalf(arena_size[1])

    # Filter
    rgray = cv.cvtColor(image,cv.COLOR_BGR2GRAY)
    _, tresh = cv.threshold(rgray, lower_black, upper_black, cv.THRESH_BINARY)

    y,x = np.shape(tresh)

    arena = cv.morphologyEx(tresh, cv.MORPH_CLOSE, kernel)

    for i in range(x):
        arena[0][i] = 0
        arena[y-1][i] = 0

    for j in range(y):
        arena[j][0] = 0
        arena[j][x-1] = 0

    
    arena = cv.erode(arena, kernel , iterations=error_expansion)
    arena = cv.resize(arena, (width, height), interpolation=cv.INTER_LINEAR)

    return tresh, arena

def getGoalPosition():
    image = getImage()
    
    # Find Mistery Machine angle
    maskBlue = cv.inRange(image, lower_blue, upper_blue) 
    goal = cv.findNonZero(maskBlue)
    goalx, goaly = goal[0,0]

    return (getHalf(goalx), getHalf(goaly))

def getRobotPosition():
    image = getImage()
    
    # Find Mistery Machine angle
    maskRed = cv.inRange(image, lower_red, upper_red) 
    front = cv.findNonZero(maskRed)
    maskGreen = cv.inRange(image, lower_green, upper_green) 
    rear = cv.findNonZero(maskGreen)

    # cv.imshow('O', image)
    # cv.imshow('G', maskGreen)
    # cv.imshow('R', maskRed)
    # cv.waitKey()
    # cv.destroyAllWindows

    if(rear is None or front is None):
        return (-1, -1), -1

    rearx, reary = rear[0,0]
    frontx, fronty = front[0,0]
    robotAngle = math.degrees(math.atan2(reary-fronty, rearx-frontx))

    # print('X', rearx, 'Y', reary)

    return (getHalf(rearx), getHalf(reary)), robotAngle

def getHalf(value):
    return int(np.floor(value/2))