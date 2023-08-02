"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module controls the flow of the program
"""

from Scans.Scans import Scans

from utilities.LinkedList import LinkedList as linkedList


def load_existing_scans():
    # This will be used when we want to open an existing scan already analyzed.
    pass


# TODO add a module for the database
# TODO add a module for the GUI

Scans = Scans("FirstScan")

Scans.load_data()
