"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module controls the flow of the program
"""

from Scans.Scans import Scans
from tqdm import tqdm


def load_existing_scans():
    # This will be used when we want to open an existing scan already analyzed.
    pass


# TODO add a module for the database
# TODO add a module for the GUI

Scans = Scans("FirstScan")

Scans.load_data()
i = 0
for j in tqdm(Scans.scans._head.data[40 if Scans.scans._head.key == "FLASH" else 500:]):
    for k in j.pixel_array_HU:
        print(k)
