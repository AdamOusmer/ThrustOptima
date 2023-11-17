"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the Scans class.

The Scans class is the main analysis class. It contains all the functions to open and analyze the DICOMDIR file.
It also contains the definition of the Scan inner class, which is used to store the data of each scan independently.

The LinkedList class is used to store the patient's IDs and the _scans associated with it in order to be able to
easily access the data and separate the data from the analysis.
"""

from backend.ThrustOptimaAnalyzer.Scans.utilities import linked_list as linked_list
from backend.ThrustOptimaAnalyzer.Scans.Exceptions import Exceptions as Ex

import pydicom
import numpy as np
import skimage as ski

from tkinter import filedialog

import os
import sys


class Scans:
    """
    Class opening and reading all the DICOMDIR file and creating a linkedList of Scan objects
    """

    # Start inner class Scan
    class _Scan:
        """
        Inner Class containing all the function to analyse each image of the scan individually.
        """

        def __init__(self, image: pydicom.FileDataset = None):
            """
            Constructor for the Scan class.
            :param image: pydicom object containing the image.
            """
            if image is None:
                raise Ex.ImageEmpty("Image is empty.")

            self._image: pydicom.FileDataset = image

            self.pixel_array_HU: np.array = (
                    self._image.pixel_array * self._image.RescaleSlope
                    + self._image.RescaleIntercept).clip(min=0, max=1).astype(np.uint8)
            # Here the image is set to HoundsField Unit (HU) and the pixel array is normalized.

            self.propensity: float = 0
            self._shaped: bool = False  # Used to check if the image has been shaped before calculating the propensity.

        def shaping(self):
            """
            Function to find the contour of object scanned and save it in the self.pixel_array_shaped.
            """

            def preprocessing():
                """
                Function to preprocess the image before finding the contour.
                By default, it will apply a gaussian filter to the image.
                return: The image preprocessed.
                """

                # Add any necessary preprocessing here

                return ski.filters.gaussian(self.pixel_array_HU, sigma=1, preserve_range=True)

            preprocessed_image = preprocessing()

            self._shaped = True  # Last line of the function to make sure that the image has been shaped correctly.

        def calc_density(self):
            """ Function to calculate the propensity of the image that has been contoured. """

            if not self._shaped:
                raise Ex.ImageNotShaped("Image has not been shaped.")

            pass

    # Class Scans starts here
    def __init__(self, name: str = None, directory: str = None, ):
        """
        Constructor for the Scans class.
        :param name: Name of the scan that will be used to be stored in the database.
        :param directory: Path to the DICOMDIR file. If not provided, it will open a file selector.
        :raises NoDirectorySelected: If the file selector is closed without selecting a file.
        :raises NoDirectoryFound: If the path provided does not exist.
        """

        # Set and create attributes
        self._dicomdir_path = None
        self._name: str = f"CTScan_{name if name is not None else 'Unknown'}"  # To be used for the database
        self._scans: linked_list = linked_list()
        self._patients_ids: set = set()  # Use a set to avoid duplicates
        self._loaded: bool = False

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
        Method to load the data from the DICOMDIR file, it will create the Scan objects and store them in the _scans
        linked list.

        This function will also order the patients per PatientID and by InstanceNumber.

        :raises AlreadyLoaded: If the data has already been loaded.
        :raises AttributeError: If the DICOM file does not contain a PatientID.
        :raises Exception: If an unknown error occurs while reading the PatientID.
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

            images = sorted(images, key=lambda image_sorter: image_sorter.InstanceNumber)

            patients_scans = linked_list()

            for patient_IDS in self._patients_ids:
                patients_scans.add([], str(patient_IDS))

            for image in images:
                patients_scans.add_to_data(self._Scan(image), image.PatientID)

            return patients_scans

        # Start of the function
        nb_picture = 0
        images_not_separated = []

        if self._loaded:
            raise Ex.AlreadyLoaded("This instance is already _loaded.")

        self._loaded = True

        dicomdir = None

        #  Dicomdir is a file that contains a summary of a FIle-Set.
        try:
            dicomdir = pydicom.dcmread(self._dicomdir_path)
        except:
            raise Ex.DicomdirError()

        for dicom in dicomdir.DirectoryRecordSequence:

            record = self._dicomdir_path.removesuffix("DICOMDIR")
            if dicom.DirectoryRecordType == "IMAGE":
                for i in dicom.ReferencedFileID:
                    record += "/" + i  # Get the absolute path to the current DICOM file in the DICOMDIR file.

                image_read = pydicom.dcmread(record)  # Read the DICOM file in other to extract the image.

                if dicom_is_image(image_read):  # Check if the DICOM file is an image.
                    # Remove the localizer and derived images for the Dose Report and Scout Scan
                    if image_read.ImageType[2] != "LOCALIZER" and image_read.ImageType[0] != "DERIVED":
                        nb_picture += 1
                        images_not_separated.append(image_read)
                else:
                    # Instead of reading the patient for all the images, we will only read it for Scout and Dose Report
                    try:
                        self._patients_ids.add(image_read.PatientID)
                    except AttributeError:
                        print("No PatientID found.")
                        sys.stdout.flush()

        self._scans = order_array_per_patients(images_not_separated)

        print(f"Number of images founded: {nb_picture}")

        return True

    def density(self, name: str = None):
        """
        Function to calculate the density of the scan.
        :param name: Name of the patient to calculate the density
        :return: Integer: Density of the scan.
        """

        if name is None:
            raise ValueError("Name cannot be None.")

        return 1

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
    def patients_ids(self):
        """
        Getter for the patients IDs.
        :return: Array of patients IDs.
        """
        return self._patients_ids

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
