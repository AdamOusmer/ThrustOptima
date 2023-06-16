"""
    Adam Ousmer, Space Concordia : Rocketry Division, 2023
    Main module for the ThrustOptima project.
    This module is used to control the flow of the program.
"""

from Scans.Scans import Scans


def load_existing_scans():
    # This will be used when we want to open an existing scan already analyzed.
    pass


# TODO add a module for the database
# TODO add a module for the GUI

Scans = Scans("FirstScan")

Scans.load_data()
