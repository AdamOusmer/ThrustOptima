"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the Scans class.

The Scans class is the main analysis class. It contains all the functions to open and analyze the DICOMDIR file.
It also contains the definition of the Scan inner class, which is used to store the data of each scan independently.

The LinkedList class is used to store the patient's IDs and the _scans associated with it in order to be able to
easily access the data and separate the data from the analysis.
"""

from tkinter import filedialog
from utilities.LinkedList import LinkedList as linkedList
import numpy as np
import pydicom
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

        def __init__(self, image: np.ndarray = None):
            """
            Constructor for the Scan class.
            :param image: pydicom object containing the image.
            """
            if image is None:
                raise Ex.ImageEmpty("Image is empty.")

            self.image: np.ndarray = image
            self.propensity: float = 0
            self.shaped_image: np.ndarray = image
            self.shaped: bool = False

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
    def __init__(self, name: str = None, directory: str = None,
                 coefficient: float = 0):  # TODO change coefficient with the one for the human head
        """
        Constructor for the Scans class.
        :param name: Name of the scan that will be used to be stored in the database.
        :param directory: Path to the DICOMDIR file. If not provided, it will open a file selector.
        :raises NoDirectorySelected: If the file selector is closed without selecting a file.
        :raises NoDirectoryFound: If the path provided does not exist.
        """

        # Set and create attributes
        self._dicomdir_path = None
        self._name: str = f"CTScan_{name if name is not None else 'Unknown'}"
        self._scans: linkedList = linkedList()
        self._patientsIDs: set = set()
        self._loaded: bool = False
        self._coefficient = coefficient

        # Getting the path to the DICOMDIR file, if not provided, it will open a file selector.
        if directory is None:
            directory = filedialog.askopenfilename()  # Open os files selector

            if not directory:  # In case the file selector is closed without selecting a file.
                raise Ex.NoDirectorySelected("No DICOMDIR selected. Instance will not be create.")

        elif not (os.path.exists(directory)):  # If the path is provided, check if it exists.
            raise Ex.NoDirectoryFound("Path does not exist. Instance will not be create.")

        self._dicomdir_path = directory  # Set the path to the DICOMDIR file if all components are valid.

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

            patients_scans = linkedList()

            for patient_IDS in self._patientsIDs:
                patients_scans.add([], str(patient_IDS))

            for image in images:
                patients_scans.add_to_data(image, image.PatientID)

            return patients_scans

        nb_picture = 0
        images_not_separated = []

        if self._loaded:
            raise Ex.AlreadyLoaded("This instance is already _loaded.")
            # TODO add a way to unload the instance if the user wants to.

        self._loaded = True

        #  Dicomdir is a file that contains a summary of a FIle-Set.
        # TODO add comments
        dicomdir = pydicom.dcmread(self._dicomdir_path)

        for dicom in dicomdir.DirectoryRecordSequence:

            record = self._dicomdir_path.removesuffix("DICOMDIR")
            if dicom.DirectoryRecordType == "IMAGE":
                for i in dicom.ReferencedFileID:
                    record += "/" + i

                image_read = pydicom.dcmread(record)

                if dicom_is_image(image_read):
                    nb_picture += 1
                    if image_read.ImageType[2] != "LOCALIZER" and image_read.ImageType[0] != "DERIVED":
                        images_not_separated.append(image_read)
                else:
                    try:
                        self._patientsIDs.add(image_read.PatientID)
                    except AttributeError:
                        print("No PatientID found.")
                    except Exception:  # TODO: Find a way to select all the exceptions that can be raised.
                        print("Error while reading the PatientID.")

        self._scans = order_array_per_patients(images_not_separated)
        print(repr(self._scans))

        print(f"Number of images founded: {nb_picture}")

    def load_image(self):
        """
        Method to load the images from each object of the linked list.
        This method will be used after the load_data method and normalize the values from the CT scan.
        Will create the instances of the Scan class.

        This is the computer vision part of the project.

        :raises NotLoaded: If the data has not been loaded yet.
        :return:
        """

        if not self._loaded:
            raise Ex.NotLoaded("Data has not been loaded yet.")

        # order the data in order of time
        print("Ordering the data in order of time.")
        self._scans.order_data_dicom_time()
        print("Data ordered.")

        # TODO normalize the data

        hWater = 0

        correction = ((self._coefficient - hWater) / hWater) * 100

        for i in self._scans.get_keys():
            for j in self._scans[i]:
                j = j / correction

    @property
    def name(self):
        """
        Getter for the name of the scan.
        :return: Name of the scan.
        """
        return self._name

    @property
    def scans(self):
        """
        Getter for the scans.
        :return: Array of Scan objects.
        """
        return self._scans

    @property
    def patientsIDs(self):
        """
        Getter for the patients IDs.
        :return: Array of patients IDs.
        """
        return self._patientsIDs

    @property
    def loaded(self):
        """
        Getter for the loaded attribute.
        :return: True if the data has been loaded, False otherwise.
        """
        return self._loaded

    @property
    def dicomdir_path(self):
        """
        Getter for the path to the DICOMDIR file.
        :return: Path to the DICOMDIR file.
        """
        return self._dicomdir_path

    @property
    def coefficient(self):
        """
        Getter for the coefficient used to normalize the data based on the Houn's level
        :return: Coefficient
        """

        return self._coefficient
