# -*- coding: utf-8 -*-
import cv2
import libqr
import numpy as np
import sys

if __name__=="__main__":

    args = sys.argv
    if len(args) == 1:
        img_path = "./img/qrcode.png"
    else:
        img_path = args[1]

    reader = libqr.QrReader()

    # obtain image data
    im = cv2.imread(img_path)
    qrs = reader.readQr(im)
    print(qrs)
    for qr in qrs:
        # do something useful with 
        pts = np.array(qr["pos"], np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(im,[pts],True,(255,0,0) , 10)

    cv2.imshow("Capture", im)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

