"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the Scans class.

The Scans class is the main analysis class. It contains all the functions to open and analyze the DICOMDIR file.
It also contains the definition of the Scan inner class, which is used to store the data of each scan independently.

The LinkedList class is used to store the patient's IDs and the _scans associated with it in order to be able to
easily access the data and separate the data from the analysis.
"""

from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    """
    Entry point of the program

    """
    pass
