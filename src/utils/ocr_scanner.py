import cv2
import pytesseract
import os
import re
import numpy as np
from pytesseract import Output


class ImagePreprocessor:
    def resize_image(self, image):
        # print('rescaling the image ... ')
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        return image

    def to_grayscale(self, image):
        # print('converting image to gray ... ')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def apply_binarization(self, image):
        # Apply threshold to get image with only b&w (binarization)
        # print('applying binarization ... ')
        image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
        return image

    def preprocess_image(self, receipt):
        image = self.resize_image(receipt)
        image = self.to_grayscale(image)
        image = self.apply_binarization(image)
        return image


def crop_image(raw_image):
    gray = cv2.cvtColor(raw_image, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    grad_y = cv2.Sobel(gray, ddepth=cv2.CV_32F, dx=0, dy=1, ksize=-1)
    gradient = cv2.subtract(grad_x, grad_y)
    gradient = cv2.convertScaleAbs(gradient)
    blurred = cv2.blur(gradient, (9, 9))
    (_, thresh) = cv2.threshold(blurred, 225, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 7))
    closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    closed = cv2.erode(closed, None, iterations=4)
    closed = cv2.dilate(closed, None, iterations=4)
    (cnts, _) = cv2.findContours(closed.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    c = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
    rect = cv2.minAreaRect(c)
    box = np.int0(cv2.boxPoints(rect))
    return raw_image[0:0 + box[0][1], :]


if __name__ == '__main__':
    image_preprocessor = ImagePreprocessor()
    image = cv2.imread(os.getcwd() + '/receipt.jpg')

    receipt_image = crop_image(image)
    receipt_image = image_preprocessor.preprocess_image(receipt_image)

    config = '-l eng --oem 1 --psm 3'
    image_text = pytesseract.image_to_string(receipt_image, config=config)
    image_text = image_text.encode('ascii', 'ignore').decode('ascii')
    print(image_text)
