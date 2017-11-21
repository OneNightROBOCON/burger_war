# -*- coding: utf-8 -*-
import zbar
import cv2


class QrReader():
    def __init__(self):
        self.scanner = zbar.ImageScanner()
        # configure the reader
        self.scanner.parse_config('enable')

    def readQr(self, im):
        '''
        read Qr code return [{"val":qrval, "pos":[x1,y1,x2,y2]}....]
        input cv2 im object BGR
        '''
        # convert BGR to GRAY
        gray_im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        height, width = gray_im.shape[:2]
        # wrap image data
        image = zbar.Image(width, height, 'Y800', gray_im.tostring())
        # scan the image for barcodes
        self.scanner.scan(image)
        results = [{"val":symbol.data, "pos":symbol.location} for symbol in image]
        return results
