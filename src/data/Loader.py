"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2026
All Rights Reserved.
******************************************************************

This module contains the Loader class which is used to load the data
from all the DICOM files in a folder that contains a DICOMDIR file.

It will also be the main controller of the data and will be used to
access, modify and delete the data using the Scan class.
"""

import os
from dataclasses import asdict
from logging import Logger
from pathlib import Path

import pandas as pd
import pydicom

from domain import ScanMetadata

_LOGGER = Logger(__name__)


class Loader:

    @staticmethod
    def get_path(path: str = None) -> Path | None:

        if not isinstance(path, str) or path is None:
            return None

        path = path.strip()

        if not path:
            return None

        if not os.path.exists(path) or not os.path.isdir(path):
            return None

        return Path(path)

    @staticmethod
    def get_files(path: Path = None) -> pydicom.FileDataset:

        if not isinstance(path, Path) or path is None:
            raise ValueError("The path provided is invalid.")

        try:
            dcm: pydicom.FileDataset = pydicom.dcmread(path / "DICOMDIR")
        except Exception:
            raise ValueError("The file you are trying to read is not compatible or might be corrupted.")

        return dcm

    @staticmethod
    def create_scan_metadata(dcm: pydicom.FileDataset, file_path: Path) -> ScanMetadata:

        if dcm is None or not isinstance(dcm, pydicom.FileDataset):
            raise ValueError("The DICOM dataset provided is invalid.")

        return ScanMetadata(id=dcm.InstanceNumber, pid=dcm.PatientID, rescale_slope=dcm.RescaleSlope,
                            rescale_intercept=dcm.RescaleIntercept, path=file_path)

    @staticmethod
    def extract_scans(path: Path) -> pd.DataFrame:

        dcm = Loader.get_files(path)

        scans = []

        for record in dcm.DirectoryRecordSequence:

            if record.DirectoryRecordType != "IMAGE":
                continue

            record_directory = path.joinpath(*record.ReferencedFileID)

            try:
                image_read = pydicom.dcmread(record_directory, stop_before_pixels=True)
            except Exception:
                _LOGGER.warning(f"Could not read DICOM file at {record_directory}. Skipping.")
                continue

            if 0x7fe00010 not in image_read:  # Pixel Data tag
                continue

            image_type = getattr(image_read, 'ImageType', [])
            if 'LOCALIZER' in image_type or 'DERIVED' in image_type:
                continue

            scan_metadata = Loader.create_scan_metadata(image_read, record_directory)

            scans.append({
                **asdict(scan_metadata),
                'metadata': scan_metadata   # Store to access pixel_array later
            }
            )

        return pd.DataFrame(scans)

    @staticmethod
    def load(path: str = None):

        if (path_ := Loader.get_path(path)) is None:    # () is used cause of walrus operator precedence
            raise FileNotFoundError("The path provided is invalid.")

        data = Loader.extract_scans(path_)

        return data
