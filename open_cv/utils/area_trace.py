import cv2 as cv
import numpy as np

def Align(image,points,width,height):
    source_points = np.float32([points])
    target_points = np.float32([[0,0],[width,0],[0,height],[width,height]])
    M = cv.getPerspectiveTransform(source_points,target_points)
    dst = cv.warpPerspective(image, M, (width,height))
    return dst