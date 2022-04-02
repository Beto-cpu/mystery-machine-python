import math
from numpy import ceil, floor
from time import sleep

maxDelta = 20

def moveRobot(HPF, position, robotAngle, arduino):
    x, y = position
    actualMin = HPF[y,x]
    pathAngle = -1
    
    if(x == -1):
        print('Not detected')
        return arduino.write(b'0') #Alto
        # print('0')

    else:
        if(HPF[y,x-1] < actualMin):
            actualMin = HPF[y,x-1]
            pathAngle = 0

        if(HPF[y-1,x] < actualMin):
            actualMin = HPF[y-1,x]
            pathAngle = 90

        if(HPF[y,x+1] < actualMin):
            actualMin = HPF[y,x+1]
            pathAngle = 180

        if(HPF[y+1,x] < actualMin):
            actualMin = HPF[y+1,x]
            pathAngle = -90

        if(HPF[y-1,x-1] < actualMin):
            actualMin = HPF[y-1,x-1]
            pathAngle = 45

        if(HPF[y-1,x+1] < actualMin):
            actualMin = HPF[y-1,x+1]
            pathAngle = 135

        if(HPF[y+1,x-1] < actualMin):
            actualMin = HPF[y+1,x-1]
            pathAngle = -45

        if(HPF[y+1,x+1] < actualMin):
            actualMin = HPF[y+1,x+1]
            pathAngle = -135
            
        if(actualMin == HPF[y,x]):
            print('Local Minimum')
            return arduino.write(b'0')

    deltaBetween = abs(pathAngle - robotAngle)
    deltaPath = 180 - abs(pathAngle)
    deltaRobot = 180 - abs(robotAngle)

    print('Robot angle: ', robotAngle,'. Path angle:', pathAngle,'. Delta Between: ', deltaBetween, '. Delta sum: ', deltaRobot+deltaPath)
        
    if(deltaBetween < maxDelta or (deltaPath + deltaRobot) < maxDelta):
        arduino.write(b'1') #Derecho
        # print('1')
        sleep(0.025)
        arduino.write(b'0') #Alto

    elif (deltaBetween < 180):
        if (robotAngle < pathAngle):
            arduino.write(b'3') #derecha
            sleep(0.015)
            arduino.write(b'0') #Alto
        else: 
            arduino.write(b'2') #Izquierda
            sleep(0.015)
            arduino.write(b'0') #Alto
    else: 
        if (robotAngle < pathAngle):
            arduino.write(b'2') #Izquierda
            sleep(0.015)
            arduino.write(b'0') #Alto
        else:
            arduino.write(b'3') #derecha
            sleep(0.015)
            arduino.write(b'0') #Alto
