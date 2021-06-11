# reading data from camera

import cv2
import logging
import os
import sys
from parameters import url

class Camera:

    def __init__(self, url=url):
        self.url = url

    def capture(self, name):
        log = ""
        status = 1 # 1 means is safe and 0 means is error

        capture = cv2.VideoCapture(self.url)
        _, frame = capture.read() # read data
        try:
            cv2.imwrite(name, frame) # save in file
            log = " image captured and saved into the {}".format(os.path.join('logs', 'main.log'))
            logging.info(log)

        except:
            log = "the image coud not save, error is type of \n {} ".format(sys.exc_info()[0])
            status = 0 
            logging.error(log)
        
        #realse capture
        capture.release()
        cv2.destroyAllWindows()
        return status, log


        

