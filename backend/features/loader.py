"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the Loader class which is used to load the data
from all the DICOM files in a folder that contains a DICOMDIR file.

It will also be the main controller of the data and will be used to
access, modify and delete the data using the Scan class.
"""

import pydicom
import time
import copy
from tkinter import filedialog

from utilities.scan import Scan




class Loader:
    def __init__(self, path: str = None):
        try:
            self._path = path if (path is not None and path.strip() is not None) else filedialog.askdirectory()
            # Path to the folder containing a DICOMDIR file
        except FileNotFoundError:
            raise FileNotFoundError("The path provided is invalid.")

        try:
            self._dcm: pydicom.FileDataset = pydicom.dcmread(self._path + "/DICOMDIR")
        except Exception:
            raise ValueError("The file you are trying to read is not compatible or might be corrupted.")

        self._patients_ids: set = set()
        self._data: dict = dict()  # Dictionary of patients with a list of scans

        self._size: int = 0

    def load(self):
        """
        Function to load the data from the DICOMDIR file into the LinkedList.
        """
        if len(self._data) != 0:
            raise ValueError("The data has already been loaded.")

        self._load()

    def _load(self):

        for dicom in self._dcm.DirectoryRecordSequence:

            if dicom.DirectoryRecordType != "IMAGE":
                continue

            record_directory = self._path

            for record in dicom.ReferencedFileID:  # Access the path to the current record
                record_directory += "/" + record

            image_read = pydicom.dcmread(record_directory)

            if getattr(image_read, 'pixel_array', None) is None:
                continue

            if image_read.ImageType[2] != "LOCALIZER" and image_read.ImageType[0] != "DERIVED":
                self._size += 1

                if self._data.get(image_read.PatientID.lower().strip()) is None:
                    self._data[image_read.PatientID.lower().strip()] = [Scan(image_read)]
                    continue

                self._data[image_read.PatientID.lower().strip()].append(Scan(image_read))

        for scans in self._data:
            self._data[scans].sort(key=lambda x: x.id)

    @property
    def size(self):
        return self._size

    @property
    def data(self):
        return copy.copy(self._data)


if __name__ == "__main__":
    # For testing purposes only
    loader = Loader("/Users/adam/Documents/Space Concordia/ThrustOptima/Scans/A")
    loader.load()
    print(loader.size)

    for patient in loader.data:
        for scan in loader.data[patient]:
            scan.shape()
            time.sleep(2)
