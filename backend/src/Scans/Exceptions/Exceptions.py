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
    def __init__(self, message: str = "Image is empty."):
        super().__init__(message)


class AlreadyLoaded(Exception):
    def __init__(self, message: str = "Data has already been loaded. Please unload the data before loading new data."):
        super().__init__(message)


class NoImageFound(Exception):
    def __init__(self, message: str = "No image found. Please load an image before using this function."):
        super().__init__(message)


class NoScanFound(Exception):
    def __init__(self, message: str = "No scan found. Please load a scan before using this function."):
        super().__init__(message)


class DangerousModification(Exception):
    def __init__(self, message: str = "This modification is dangerous and can lead to data loss. "
                                      " Please use the dedicated "
                                      "function to do so."):
        super().__init__(message)


class NotLoaded(Exception):
    def __init__(self, message: str = "No data has been loaded yet. Please load data before using this function."):
        super().__init__(message)


class ImageNotShaped(Exception):
    def __init__(self,
                 message: str = "The image has not been shaped yet. Please shape the image before using this function."):
        super.__init__(message)
