# ALL needed parameters set in this file.
# change this parameters as you want 

import numpy as np 
import os

# RTSP camera url
url = 0 

# there is two types of kernels for using in the erosion phase
thin_kernel = np.ones((3,3),np.uint8)
wide_kernel = np.ones((5,5),np.uint8)

# min amd max of pixel in a contour for remove small and big contours
minimum_contour_size = 1000 
maximum_contour_size = 25000 

# pyteseract installed path
pyteseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# persian numbers
persian_numbers = {
    "۰":1,
    "۱":1,
    "۲":1,
    "۳":1,
    "۴":1,
    "۵":1,
    "۶":1,
    "۷":1,
    "۸":1,
    "۹":1
}

# minimum and maximum number of persian numbers for accept as a plate
minimum_persian_numbers_count = 4
maximum_persian_numbers_count = 8

# db variables
db_path = os.path.join("db", "iCCard.mdb")
db_pass = "168168"

# log size
log_file_size = 50 * 1025 * 1024