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

    def __init__(self, restore_state: bool = False):
        """
        This is the constructor of the Controller class. It will be used to initialize the Controller object.
        """
        self._scans = None

        if restore_state:
            self.restore_state()
        else:
            self._scans = scans.Scans()

    def load_existing_scans(self, name: str = None):
        """
        This function will load an existing scan from the database.
        :raises ValueError: If the name is empty or None
        """

        if not name.strip() or name is None:
            raise ValueError("Name cannot be empty")

    def restore_state(self, path: str = None):
        pass

        def restore_scan(path: str = None):
            pass
