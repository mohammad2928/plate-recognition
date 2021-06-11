import cv2
import numpy as np
import os
import pytesseract
import logging

from parameters import minimum_contour_size, maximum_contour_size
from parameters import persian_numbers, minimum_persian_numbers_count 
from parameters import maximum_persian_numbers_count


class ImageProcessing:
    # get the image
    # convert to gray
    # make thresh
    # make erosion
    # extract contours 
    # check for plate box 

    def __init__(self):
        pass

    def read_image(self, image_path):
        img = cv2.imread(image_path)
        return img

    def filter_contours(self, contours):
        out = [] 
        for i in contours:
            if cv2.contourArea(i)  > minimum_contour_size and cv2.contourArea(i)  < maximum_contour_size :
                out.append(i)
        return np.array(out)

    def convert_to_gray(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return gray

    def threshold(self, gray):
        _, thresh = cv2.threshold(gray, 40, 240, cv2.THRESH_BINARY)
        return thresh

    def erosion(self, thresh, kernel):
        erosion = cv2.erode(thresh, kernel, iterations = 1) 
        return erosion

    def extract_contours(self, erothion, thresh, img, start_index):
        contours, hierarchy = cv2.findContours(erothion, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        fit_contours = self.filter_contours(contours)
        contours = []
        orig_croped_contours = []

        for (i,c) in enumerate(fit_contours):
            x,y,w,h= cv2.boundingRect(c)
            cropped_contour= erothion[y:y+h, x:x+w]
            orig_croped_contours.append(img[y:y+h, x:x+w])
            image_name= os.path.join("temp", str(start_index+1) + ".jpg")
            cv2.imwrite(image_name, cropped_contour)
            contours.append(image_name)
            logging.info("image {} saved in the temp folder".format(image_name))
            start_index += 1
        return contours, orig_croped_contours

    def save_image(self, img, name):
        cv2.imwrite(name, img)
        logging.info("image {} saved in the temp folder".format(img))

class OCR:
    
    def __init__(self):
        pass

    def extract_text(self, img):
        text = pytesseract.image_to_string(
            img, config='-l fas-tune-float --oem 1 --psm 6'
        )
        return text

    def text_checking(self, text):
        count = 0
        for i in text:
            if persian_numbers.get(i, 0):
                count += 1
        if count < minimum_persian_numbers_count or count > maximum_persian_numbers_count: # the text is not a plate
            return 0
        return 1 # the text is a plate