"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module is the main controller of the scans module. It contains the definition of the Controller class that will
be used in the thrust_optima.py module a Flask backend. It will be used to control the lifecycle of the scans module.
"""

from .scans import Scans


class Controller:

    def __init__(self):
        """
        This is the constructor of the Controller class. It will be used to initialize the Controller object.
        """
        self._scans = None

    def edge_detection(self, name:str = None):
        """
        This function will analyze the scan and return the results based on the name of the scan.
        :param name:
        :return: Integer:
        """
        pass

    def density(self, name:str = None):
        """
        This function will analyze the scan and return the results based on the name of the scan.
        :param name:
        :return: Integer:
        """
        if not name.strip() or name is None:
            raise ValueError("Name cannot be empty")

        return self._scans.density(name)

    def save(self, path: str = None):
        pass
