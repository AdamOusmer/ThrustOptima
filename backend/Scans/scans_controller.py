"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module controls the flow of the program
"""

from scans import Scans
from tqdm import tqdm
import matplotlib.pyplot as plt


def load_existing_scans():
    # This will be used when we want to open an existing scan already analyzed.
    pass


def restore_state():
    # This will be used when we want to open an existing scan already analyzed.
    pass


def restore_scan():
    # This will be used when we want to open an existing scan already analyzed.
    pass


# TODO add a module for the database
# TODO add a module for the GUI

Scans = Scans("FirstScan")

Scans.load_data()
i = 0
for j in tqdm(Scans.scans._head.data[40 if Scans.scans._head.key == "FLASH" else 500:]):
    j.shaping()

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.imshow(j.pixel_array_HU, cmap="gray")
    ax.plot((j._edges[1])[:, 1], (j._edges[1])[:, 0], '-b', lw=3)
    ax.set_xticks([]), ax.set_yticks([])
    ax.axis([0, j.pixel_array_HU.shape[1], j.pixel_array_HU.shape[0], 0])

    plt.show()

if __name__ == '__main__':
    restore_state()
