import unittest
import libqr
import cv2

class TestLibqr(unittest.TestCase):
    def setUp(self):
        self.test_im = cv2.imread("./img/qrcode.png")
        pass

    def tearDown(self):
        pass

    def test_read_qr(self):
        reader = libqr.QrReader()
        result = reader.readQr(self.test_im)
        self.assertEqual(result, "ONE-NIGHT-ROBOCON")

if __name__ == '__main__':
    unittest.main()
