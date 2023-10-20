"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the Flask application that will be used as the backend for the thrust_optima
project. It will run on the WSGI server and will be used to communicate with the Electron frontend. It will also be
used to communicate with the database.

This module will also contain the entry point of the program and it will control the lifecycle of the software.
"""
from flask import Flask
import sys
import signal

from Scans.scans_controller import Controller

app = Flask(__name__)
controller = Controller()


@app.route('/')
def index():
    """
    Entry point of the program
    :return: None
    """
    print("Hello World!")
    return "Set"


@app.route('/cleanup', methods=['POST'])
def close():
    """
    Exit point of the program. This function will be called when the user closes the program to ensure that all
    resources are properly closed and saved.
    :return: None
    """
    print("Closing...")
    sys.stdout.flush()

    return "Closed"


signal.signal(signal.SIGTERM, close())
