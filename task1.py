###############
##Design the function "findRotMat" to  return 
# 1) rotMat1: a 2D numpy array which indicates the rotation matrix from xyz to XYZ 
# 2) rotMat2: a 2D numpy array which indicates the rotation matrix from XYZ to xyz 
#It is ok to add other functions if you need
###############

import numpy as np
import cv2

def findRotMat(alpha, beta, gamma):
    #......
    # xyz --> XYZ
    
    Rz = np.array([
        [np.cos(np.radians(alpha)), -np.sin(np.radians(alpha)), 0],
        [np.sin(np.radians(alpha)),  np.cos(np.radians(alpha)), 0],
        [          0,            0, 1]])
    Rxdash = np.array([
        [1,            0,             0],
        [0, np.cos(np.radians(beta)), -np.sin(np.radians(beta))],
        [0, np.sin(np.radians(beta)),  np.cos(np.radians(beta))]])

    Rzdoubledash = np.array([
        [np.cos(np.radians(gamma)), -np.sin(np.radians(gamma)), 0],
        [np.sin(np.radians(gamma)),  np.cos(np.radians(gamma)), 0],
        [          0,            0, 1]])


    rotmat1 = Rzdoubledash.dot(Rxdash.dot(Rz))


    #XYZ ---> xyz

    Rz = np.array([
        [np.cos(np.radians(alpha)), np.sin(np.radians(alpha)), 0],
        [-np.sin(np.radians(alpha)),  np.cos(np.radians(alpha)), 0],
        [          0,            0, 1]])
    Rxdash = np.array([
        [1,            0,             0],
        [0, np.cos(np.radians(beta)), np.sin(np.radians(beta))],
        [0, -np.sin(np.radians(beta)),  np.cos(np.radians(beta))]])

    Rzdoubledash = np.array([
        [np.cos(np.radians(gamma)), np.sin(np.radians(gamma)), 0],
        [-np.sin(np.radians(gamma)),  np.cos(np.radians(gamma)), 0],
        [          0,            0, 1]])

    rotmat2 = Rz.dot(Rxdash.dot(Rzdoubledash))
    
    return rotmat1,rotmat2


if __name__ == "__main__":
    alpha = 45
    beta = 30
    gamma = 60
    rotMat1,rotMat2 = findRotMat(alpha, beta, gamma)
    
    print(rotMat1)
    print(rotMat2)
