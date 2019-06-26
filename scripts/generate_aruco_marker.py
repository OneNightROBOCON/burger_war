#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2
import numpy as np

aruco = cv2.aruco
dictionary = aruco.getPredefinedDictionary(aruco.DICT_ARUCO_ORIGINAL)

def arGenerator(id):
    fileName = "./onigiri_war/models/tags/" + ("0000" + str(id))[-4:] + ".png"
    brank = np.zeros((130,130), dtype=np.uint8) + 255

    generator = aruco.drawMarker(dictionary, id, 100)
    brank[15:115, 15:115] = generator

    cv2.imwrite(fileName, brank)

    img = cv2.imread(fileName)
    cv2.imshow('ArMaker',img)
    cv2.waitKey(10)

for i in range(250):
    arGenerator(i)

