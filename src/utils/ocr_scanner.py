import cv2
import pytesseract
import numpy as np

import os
import re
import json


class ImagePreprocessor:
    def resize_image(self, image):
        # print('rescaling the image ... ')
        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_LINEAR)
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

    def crop_image(self, raw_image):
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
        raw_image[box[0][1]:, :] = 255
        return raw_image


def is_number(s):
    try:
        float(s)
    except ValueError:
        return False
    return True


def detect(image_path: str):
    image_preprocessor = ImagePreprocessor()
    receipt_image = cv2.imread(image_path)

    receipt_image = image_preprocessor.crop_image(receipt_image)

    receipt_image = image_preprocessor.preprocess_image(receipt_image)

    config = '-l eng --oem 1 --psm 3 -c preserve_interword_spaces=1'
    image_text = pytesseract.image_to_string(receipt_image, config=config)
    image_text = image_text.encode('ascii', 'ignore').decode('ascii')
    image_text = re.sub(r'<a>', '<A>', image_text)
    lines = image_text.split('\n')
    # removing redundant lines
    index = 0
    for line in lines:
        if '<A>' in line:
            break
        index += 1
    lines = lines[index:]

    # filtering items
    index = 0
    for line in lines:
        if 'SUBTOTAL' in line:
            break
        index += 1

    text = '\n'.join(lines)
    text = re.sub(r'\n+', '\n', text)
    items = []
    matches = re.finditer(r'.*<A>(\n?.*\n?){2}', text, flags=re.MULTILINE)
    for match_num, match in enumerate(matches, start=1):
        item_text = match.group()
        item_name = re.findall(r'.+<A>', item_text)[0].strip()
        price = ''
        is_price_found = False
        description = ''
        for item_line in item_text.split('\n'):
            if '<A>' in item_line:
                split = item_line.split('<A>')
                if len(split) > 1:
                    if is_number(split[1].strip()):
                        price = split[1].strip()
                        is_price_found = True
            else:
                if is_price_found:
                    description += item_line + '\n'
        if not is_price_found:
            matches = re.finditer(r' +[0-9]+\.([0-9]+)?$', item_text, re.MULTILINE)
            for new_match_num, new_match in enumerate(matches, start=1):
                price = new_match.group().strip()
                break
            description = item_text.replace(price, '')
            description = description.replace(item_name, '')

        description = description.rstrip().strip()
        item = {
            'item': item_name,
            'price': price,
            'description': description

        }
        items.append(item)
    output = dict()
    for i in range(index, len(lines)):
        data = re.split(r'  +', lines[i])
        if len(data) > 1:
            output[data[0]] = data[1]
    output['items'] = items

    return json.dumps(output)


if __name__ == '__main__':
    print(detect(os.getcwd() + '/receipt1.jpg'))
