# main file 

import logging
import os
import pytesseract
import time
import cv2 
import datetime
from imp import reload

from camera import Camera
from utilities import Initialize, Utiles
from parameters import pyteseract_path, thin_kernel, wide_kernel, log_file_size
from image_processing import OCR, ImageProcessing
from db import DB
from logging.handlers import RotatingFileHandler


def main():
    # initilaize
    initiate = Initialize() 
    utils = Utiles()
    logging.info("folders initialized")

    # initialize tesseract
    pytesseract.pytesseract.tesseract_cmd = pyteseract_path
    logging.info("tesseract initialized")

    log_file_name = os.path.join('logs', 'logs.log')
    reload(logging)

    logging.basicConfig(handlers=[logging.FileHandler(
                                    filename=log_file_name, 
                                                 encoding='utf-8', mode='a+',
                                                ),
                                                RotatingFileHandler(filename=log_file_name, maxBytes=log_file_size, backupCount=0)
                                ],
                    
                    format='%(asctime)s - %(message)s',
                    datefmt='%d-%b-%y %H:%M:%S', 
                    level=logging.INFO)
    C = Camera(0)
    ocr = OCR()

    db = DB()
    cursor, conn = db.connect()
    logging.info("db initialized")

    image_proc = ImageProcessing()
    temp_image_path = os.path.join("temp", "capture.jpg")

    while 1:
        C.capture(temp_image_path)

        utils.checking_log_file(log_file_name, log_file_size)
        # for file in os.listdir("test_folder"):
        #     # print("files is {}".format(file))
        #     temp_image_path = os.path.join("test_folder", file) 

        start_index = 0
        img = image_proc.read_image(temp_image_path)
        gray = image_proc.convert_to_gray(img)
        thresh = image_proc.threshold(gray)
        erothion = image_proc.erosion(thresh, thin_kernel)

        contours, orig_croped_contours = image_proc.extract_contours(erothion, thresh, img, start_index)
        start_index += len(contours)
        erothion = image_proc.erosion(thresh, wide_kernel)
        contours1, orig_croped_contours1 = image_proc.extract_contours(erothion, thresh, img, start_index)
        contours += contours1
        orig_croped_contours += orig_croped_contours1


        for i, contour in enumerate(contours):
            contour_img = image_proc.read_image(contour)
            persain_text = ocr.extract_text(contour_img) 
            if ocr.text_checking(persain_text):
                print("plate is recognize and text is {}".format(persain_text))
                plate_name = os.path.join("plate_images", utils.randome_name()+".jpg")
                image_proc.save_image(orig_croped_contours[i], plate_name)

                # save plate in plate_images dir 
                query = "INSERT INTO Plate_table ([image_path], [plate_text],[capture_date]) VALUES (?,?, ?)"
                values = (plate_name, persain_text, datetime.datetime.now())
                db.insert(cursor, conn, query, values)

                # remove all files in temp folder
                folder_path = os.path.join("temp", "*")
                utils.remove_folder_contents(folder_path)
                break
            else:
                #remove file in temp folder
                utils.remove_file(contour)

        logging.info("no plate found in image")

if __name__ == "__main__":
    main()