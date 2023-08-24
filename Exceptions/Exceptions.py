"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************
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
