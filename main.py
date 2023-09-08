"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module controls the flow of the program
"""

from Scans.Scans import Scans
from tqdm import tqdm
import matplotlib.pyplot as plt
import time


def load_existing_scans():
    # This will be used when we want to open an existing scan already analyzed.
    pass


# TODO add a module for the database
# TODO add a module for the GUI

Scans = Scans("FirstScan")

Scans.load_data()

for i in tqdm(range(len(Scans.scans.head.data))):
    plt.imshow(Scans.scans.head.data[i].pixel_array, cmap="bone")
    plt.show()
    time.sleep(10) if i % 4 == 0 else None  # To avoid http error 429: too many requests
