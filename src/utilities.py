import os
import uuid
import glob
import logging

class Initialize:

    def __init__(self):
        self.make_folders()

    def make_folders(self):
        """
        the followig folders will be created
        """
        if not os.path.exists('temp'):
            os.makedirs('temp')

        if not os.path.exists('logs'):
            os.makedirs('logs')

        if not os.path.exists('plate_images'):
            os.makedirs('plate_images')


class Utiles:
    
    def __init__(self):
        pass

    def randome_name(self):
        return str(uuid.uuid4())

    def remove_file(self, file_path):
        if os.path.exists(file_path):
            os.remove(file_path)
            logging.warning("file {} removed".format(file_path))

    def remove_folder_contents(self, folder_path):
        files = glob.glob(folder_path)
        for f in files:
            os.remove(f)
        logging.warning("all files in the folder {} removed".format(folder_path))

    def checking_log_file(self, log_path, log_file_size):
        if os.stat(log_path).st_size >= log_file_size:
            open(log_path, 'w').close()

    