"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of all the custom exceptions that will be used in the different modules of the
project.
"""


class NoDirectorySelected(Exception):
    pass


class NoDirectoryFound(Exception):
    pass


class ImageEmpty(Exception):
    pass


class AlreadyLoaded(Exception):
    pass


class NoImageFound(Exception):
    pass


class NoScanFound(Exception):
    pass


class DangerousModification(Exception):
    def __init__(self, message: str = "This modification is dangerous and can lead to data loss. "
                                      " Please use the dedicated "
                                      "function to do so."):
        super().__init__(message)


class NotLoaded(Exception):
    def __init__(self, message: str = "No data has been loaded yet. Please load data before using this function."):
        super().__init__(message)
