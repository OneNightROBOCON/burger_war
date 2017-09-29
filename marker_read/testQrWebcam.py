# -*- coding: utf-8 -*-
import libqr # local lib

import cv2
import numpy as np
import sys

if __name__=="__main__":

    reader = libqr.QrReader()
    cap = cv2.VideoCapture(0)

    if cap.isOpened() is False:
        print("IO Error")
        sys.exit()

    cv2.namedWindow("Capture", cv2.WINDOW_AUTOSIZE)

    while cap.isOpened():

        ret, im = cap.read()

        if ret == False:
            continue
        # read QR code
        qrs = reader.readQr(im)
        if qrs:
            print(qrs)
        for qr in qrs:
            # do something useful with 
            pts = np.array(qr["pos"], np.int32)
            pts = pts.reshape((-1,1,2))
            cv2.polylines(im,[pts],True,(255,0,0) , 10)

        cv2.imshow("Capture", im)

        if cv2.waitKey(33) >= 0:
            break
    else:
        print("cap is not opend")

    cv2.destroyAllWindows()
