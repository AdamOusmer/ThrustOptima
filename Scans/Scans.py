"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the Scans class.

The Scans class is the main analysis class. It contains all the functions to open and analyze the DICOMDIR file.
It also contains the definition of the Scan inner class, which is used to store the data of each scan independently.

The LinkedList class is used to store the patient's IDs and the scans associated with it in order to be able to
easily access the data and separate the data from the analysis.
"""

from tkinter import filedialog
import pydicom
import numpy as np  # needed for pydicom to work
import Exceptions.Exceptions as Ex
import os


class Scans:
    """
    Class opening and reading all the DICOMDIR file and creating an array of Scan objects
    """

    # Start inner class Scan
    class Scan:
        """
        Inner Class containing all the function to analyse the image for the opened image.
        """

        def __init__(self, image):
            """
            Constructor for the Scan class.
            :param image: pydicom object containing the image.
            """
            if image is None:
                raise Ex.ImageEmpty("Image is empty.")

            self.image = image
            self.propensity = 0
            self.shaped_image = None
            self.shaped = False

        def shaping(self):
            """
            Function to find the contour of object scanned.
            TODO do the function in the scan class
            """
            self.shaped = True
            pass

        def cal_propensity(self):
            """ Function to calculate the propensity of the image that has been contoured. """

            if not self.shaped:
                print("Warning: Image has not been shaped yet.")

            pass

        def weak_spot(self):
            """
            To develop and save image in an easily readable image file.
            TODO not sure to add it, will be in the official release or in the first major update
            """
            pass

    # Class Scans starts here
    def __init__(self, name: str = "", directory: str = None):
        """
        Constructor for the Scans class.
        :param name: Name of the scan that will be used to be stored in the database.
        :param directory: Path to the DICOMDIR file. If not provided, it will open a file selector.
        :raises NoDirectorySelected: If the file selector is closed without selecting a file.
        :raises NoDirectoryFound: If the path provided does not exist.
        """

        # Set and create attributes
        self.dicomdir_path = None
        self.name = f"CTScan_{name}"
        self.scans = []
        self.patientsIDs = set()
        self.loaded = False

        # Getting the path to the DICOMDIR file, if not provided, it will open a file selector.
        if directory is None:
            directory = filedialog.askopenfilename()  # Open os files selector

            if not directory:  # In case the file selector is closed without selecting a file.
                raise Ex.NoDirectorySelected("No folder selected. Instance will not be create.")

        elif not (os.path.exists(directory)):  # If the path is provided, check if it exists.
            raise Ex.NoDirectoryFound("Path does not exist. Instance will not be create.")

        self.dicomdir_path = directory  # Set the path to the DICOMDIR file if all components are valid.

    def load_data(self):
        """
        Method to load the data from the DICOMDIR file.
        WARNING: use this method only after the constructor.
        WARNING: This method is not working yet.
        """

        def dicom_is_image(dicom_image):
            """
            Internal function to check if the DICOM file is an image.
            :param dicom_image: pydicom object to check.
            :return: True if the DICOM file is an image, False otherwise.
            """
            return getattr(dicom_image, 'pixel_array', None) is not None

        def order_array_per_patients(images):
            """
            Internal function to order the images per patients.
            :param images: Array of pydicom objects that contain an image.
            :return: Array of pydicom objects ordered per patients.
            """

            ordered_images = []

            for _ in self.patientsIDs:
                ordered_images.append([])

            for image in images:
                if image.PatientID in self.patientsIDs:
                    pass

            # TODO: waiting for LinkedList to be done.
            return ordered_images

        nb_picture = 0
        images_not_separated = []

        if self.loaded:
            raise Ex.AlreadyLoaded("This instance is already loaded.")
            # TODO add a way to unload the instance if the user wants to.

        self.loaded = True

        #  Dicomdir is a file that contains a summary of a FIle-Set.
        dicomdir = pydicom.dcmread(self.dicomdir_path)

        for dicom in dicomdir.DirectoryRecordSequence:

            record = self.dicomdir_path.removesuffix("DICOMDIR")
            if dicom.DirectoryRecordType == "IMAGE":
                for i in dicom.ReferencedFileID:
                    record += "/" + i

                image_read = pydicom.dcmread(record)

                if dicom_is_image(image_read):
                    nb_picture += 1
                    images_not_separated.append(image_read)
                else:
                    try:
                        self.patientsIDs.add(image_read.PatientID)
                    except AttributeError:
                        print("No PatientID found.")
                    except Exception:  # TODO: Find a way to select all the exceptions that can be raised.
                        print("Error while reading the PatientID.")

        # TODO: Find a way to load the images from the DICOMDIR file.

        print(f"Number of images founded: {nb_picture}")
