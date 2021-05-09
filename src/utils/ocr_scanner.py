import cv2
import pytesseract


class ImagePreprocessor:
    def resize_image(self, image):
        print('rescaling the image ... ')
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        return image

    def to_grayscale(self, image):
        print('converting image to gray ... ')
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image

    def apply_binarization(self, image):
        # Apply threshold to get image with only b&w (binarization)
        print('applying binarization ... ')
        image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)[1]
        return image

    def preprocess_image(self, receipt):
        image = self.resize_image(receipt)
        image = self.to_grayscale(image)
        image = self.apply_binarization(image)
        return image


if __name__ == '__main__':
    import os

    image_preprocessor = ImagePreprocessor()
    receipt_image = cv2.imread(os.getcwd() + '/receipt.jpg')
    receipt_image = image_preprocessor.preprocess_image(receipt_image)

    config = '-l eng --oem 1 --psm 3'
    image_text = pytesseract.image_to_string(receipt_image, config=config)
    image_text = image_text.encode('ascii', 'ignore').decode('ascii')
    print(image_text)
