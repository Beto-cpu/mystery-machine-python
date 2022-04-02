import numpy as np
from numpy.core.fromnumeric import shape
arena_size = (187,100) #Tambien esta en image analysis

def getPathMatrix(matrix, goal, iterations):
    height, width = shape(matrix)
    goalx, goaly =  goal
    matrix = np.minimum(matrix,1)
    HPF = ~matrix+2
    HPF = HPF.astype('float64')

    for w in range(iterations):
        for i in range(1,width-1):
            for j in range(1,height-1):
                if(HPF[j,i]!=1 and not(j==goaly and i==goalx )):
                    HPF[j,i] = (HPF[j-1,i]+HPF[j,i-1]+HPF[j+1,i]+HPF[j,i+1])/4

    np.savetxt("HarmonicFields.csv", HPF, delimiter=",")

    return HPF
