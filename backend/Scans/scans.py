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

# TODO add load function from database

from tkinter import filedialog
from .utilities.linked_list import LinkedList as linkedList
from .Exceptions import Exceptions as Ex
import numpy as np
import skimage as ski
import matplotlib.pyplot as plt
import pydicom
import os
import sys
import cv2


class Scans:
    """
    Class opening and reading all the DICOMDIR file and creating an array of Scan objects
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

            self._edges: list = []
            
            self.propensity: float = 0
            self._shaped: bool = False  # Used to check if the image has been shaped before calculating the propensity.

        def shaping(self, depth: int = 250, multi_snake: bool = True):
            """
            Function to find the contour of object scanned and save it in the self.pixel_array_shaped.
            :param depth: Size of the snake that will be used to find the contour.
            :param multi_snake: If True, the snake will be used to find an internal contour.
            """

            def preprocessing():
                """
                Function to process the image using the Gradient Vector Flow algorithm.
                return: The image preprocessed.
                """

                cv2.Sobel(self.pixel_array_HU, 6, 1, 0, ksize=5)

                return ski.filters.gaussian(self.pixel_array_HU, sigma=1, preserve_range=True)

            def gvf():
                """
                Function to calculate the Gradient Vector Flow of the image.
                """

                center = (self._image.Columns // 2, self._image.Rows // 2)
                # Create theta values
                theta = np.linspace(0, 2 * np.pi, depth)

                # Create small_snake and large_snake arrays
                small_snake = np.column_stack(
                    (center[0] + 100 * np.cos(theta), center[1] + 100 * np.sin(theta))) if multi_snake else None
                large_snake = np.column_stack((center[0] + (self._image.Columns - self._image.Columns / 1.5) * np.cos(
                    theta), center[1] + (self._image.Columns - self._image.Columns / 1.5) * np.sin(theta)))

                blurred = preprocessing()

                small_defined_snake = ski.segmentation.active_contour(blurred, small_snake, alpha=0.015, beta=5,
                                                                      gamma=0.01) if multi_snake else None
                large_defined_snake = ski.segmentation.active_contour(blurred, large_snake, alpha=10, beta=20,
                                                                      gamma=0.01)

                return small_defined_snake, large_defined_snake

            gvf_output = gvf()

            if multi_snake:
                self._edges.append(gvf_output[0])
            self._edges.append(gvf_output[1])

            self._shaped = True  # Last line of the function to make sure that the image has been shaped correctly.

        def cal_propensity(self):
            """ Function to calculate the propensity of the image that has been contoured. """

            if not self._shaped:
                print("Warning: Image has not been shaped yet.", file=sys.stderr)

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
        self._scans: linkedList = linkedList()
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

            patients_scans = linkedList()

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

        #  Dicomdir is a file that contains a summary of a FIle-Set.
        dicomdir = pydicom.dcmread(self._dicomdir_path)

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

        self._scans = order_array_per_patients(images_not_separated)

        print(f"Number of images founded: {nb_picture}")

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
