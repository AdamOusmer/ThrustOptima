"""
******************************************************************
Copyright Adam Ousmer for Space Concordia: Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the code for the GUI and it is use for all user's interactions excluding the request for the path
of the dicomdir file when the Scan object is being initialized.
"""

import tkinter as tk


class Root:
    """ Class that contain the main window of the program and all related functions """

    def __init__(self, name: str = None):
        self._root = tk.Frame()
        self._name = name if name is not None else "ThrustOptima"

    def show(self):
        self._root.mainloop()

    def close(self):
        """ Function"""
        self._root.quit()
