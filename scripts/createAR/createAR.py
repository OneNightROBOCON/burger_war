#!/usr/bin/env python
# -*- coding: utf-8 -*
import cv2
aruco = cv2.aruco
dir(aruco)

#dictionary = aruco.getPredefinedDictionary(aruco.DICT_4X4_50)

dictionary = aruco.getPredefinedDictionary(aruco.DICT_7X7_50)

for i in range(50):
    marker = aruco.drawMarker(dictionary, i, 64)
    #cv2.imshow('0.64', marker)
    cv2.imwrite(str(i)+'.png', marker)


"""
marker = aruco.drawMarker(dictionary, 1, 64)
cv2.imshow('1.64', marker)
cv2.imwrite('1.64.png', marker)

marker = aruco.drawMarker(dictionary, 2, 64)
cv2.imshow('2.64', marker)
cv2.imwrite('2.64.png', marker)

marker = aruco.drawMarker(dictionary, 3, 64)
cv2.imshow('3.64', marker)
cv2.imwrite('3.64.png', marker)

marker = aruco.drawMarker(dictionary, 4, 64)
cv2.imshow('4.64', marker)
cv2.imwrite('4.64.png', marker)

cv2.waitKey(0)
cv2.destroyAllWindows()
"""
