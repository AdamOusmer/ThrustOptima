"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module is the main controller of the scans module. It contains the definition of the Controller class that will
be used in the thrust_optima.py module a Flask backend.
"""

from .scans import Scans


class Controller:

    def __init__(self):
        """
        This is the constructor of the Controller class. It will be used to initialize the Controller object.
        """
        self._scans = None

    def restore_scan(self, path: str = None):
        """
        This function will load an existing scan from the database.
        :raises ValueError: If the name is empty or None
        """

        if not path.strip() or path is None:
            raise ValueError("Name cannot be empty")

        self._scans = Scans(path)

    def save(self, path: str = None):
        pass
