import cv2
import os
import numpy as np
from src.settings import MEDIA_ROOT

width = 640
height = 480


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 10, 10)
    # kernel = np.ones((5, 5))
    # imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    # imgThres = cv2.erode(imgDial,kernel, iterations=1)
    return imgCanny


def getContours(img):
    biggest = np.array([])
    maxArea = 0
    maxCnt = np.array([])
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        print(area)
        if area > 500:

            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
                maxCnt = cnt

    return biggest


def reorder(myPoints):
    myPoints = myPoints.reshape((4, 2))
    myPointsNew = np.zeros((4, 1, 2), np.int32)
    add = myPoints.sum(1)
    myPointsNew[0] = myPoints[np.argmin(add)]
    myPointsNew[3] = myPoints[np.argmax(add)]
    diff = np.diff(myPoints, axis=1)
    myPointsNew[1] = myPoints[np.argmin(diff)]
    myPointsNew[2] = myPoints[np.argmax(diff)]
    return myPointsNew


def getWarp(img, bigest):
    bigest = reorder(bigest)
    pts1 = np.float32(bigest)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOut = cv2.warpPerspective(img, matrix, (width, height))
    return imgOut


def ImageModule(path):
    # path = os.path.join(MEDIA_ROOT, path[8:])
    # image = cv2.imread(path)
    image = cv2.imread("D:\ML\computer vision\CV2_learn\src\image/readingCat.jpg")
    image = cv2.resize(image, (width, height))
    imageContour = image.copy()
    imgCanny = preProcessing(image)
    biggest = getContours(imgCanny)
    cv2.drawContours(imageContour, biggest, -1, (255, 0, 0), 3)
    print(biggest)
    imgWarp = getWarp(image, biggest)
    return imgWarp
    # cv2.imshow('image', imgWarp)
    # cv2.waitKey(0)
