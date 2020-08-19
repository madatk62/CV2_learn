import cv2
import os
import numpy as np
import base64
from src.settings import MEDIA_ROOT

width = 480
height = 640


def preProcessing(img):
    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
    imgCanny = cv2.Canny(imgBlur, 80, 200)
    # kernel = np.ones((5, 5))
    # imgDial = cv2.dilate(imgCanny, kernel, iterations=2)
    # imgThres = cv2.erode(imgDial,kernel, iterations=1)
    return imgCanny


# Xác định đường biên    của ảnh và trả về khung hình chữ nhật lớn nhất
def getContours(img):
    biggest = np.array([])
    maxArea = 0
    maxCnt = np.array([])
    contours, hierarchy = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)
            if area > maxArea and len(approx) == 4:
                biggest = approx
                maxArea = area
                maxCnt = cnt

    return biggest


# sắp xếp lại vị trí của toạ độ theo định dạng của toạ độ ([[0, 0], [width, 0], [0, height], [width, height]])
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


# warp khung lớn nhất vào image
def getWarp(img, bigest):
    bigest = reorder(bigest)
    pts1 = np.float32(bigest)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    imgOut = cv2.warpPerspective(img, matrix, (width, height))
    return imgOut


def ImageModule(path):
    path = os.path.join(MEDIA_ROOT, path[8:])
    image = cv2.imread(path)
    image = cv2.resize(image, (width, height))
    imageContour = image.copy()
    imgCanny = preProcessing(image)
    biggest = getContours(imgCanny)
    if len(biggest) > 0:
        cv2.drawContours(imageContour, biggest, -1, (255, 0, 0), 3)
        imgWarp = getWarp(image, biggest)
        retval, img_arr = cv2.imencode('.jpg', imgWarp)
        img_as_base64 = base64.b64encode(img_arr)
        return {"success": True,
                "result": img_as_base64}
    else:
        return {
            "success": False,
            "message": "can't detect the image"}

    # cv2.imshow('image', imgWarp)
    # cv2.waitKey(0)
