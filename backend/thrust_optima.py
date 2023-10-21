"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the Flask application that will be used as the backend for the thrust_optima
project. It will run on the WSGI server and will be used to communicate with the Electron frontend. It will also be
used to communicate with the database.

This module will also contain the entry point of the program and it will control the lifecycle of the software.

To allow the frontend to access the console output, at the end of each method, the stdout buffer will be flushed
to ensure that the output is sent to the frontend in real time.
"""

from flask import Flask
from waitress import serve

import sys
import socket
import json

from Scans.scans_controller import Controller

app = Flask(__name__)
controller = Controller()
port = None


@app.route('/')
def index():
    """
    Entry point of the program
    :return: None
    """
    print("port=" + str(port))
    sys.stdout.flush()
    return port


@app.route('/load', methods=['POST'])
def load(path: str = None):
    """
    This function will load an existing scan from the database.
    :raises ValueError: If the name is empty or None
    """

    if not path.strip() or path is None:
        raise ValueError("Path cannot be empty")

    controller.restore_scan(path)


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


# Waitress server

def find_available_port():
    """
    This function will find an available port to run the server on.
    :return: The port number
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    new_port = sock.getsockname()[1]
    sock.close()

    return new_port


if __name__ == '__main__':
    print("Starting server...", file=sys.stdout)
    sys.stdout.flush()
    try:
        serve(app, host='localhost', port=5000)
    except OSError as e:
        if e.errno == 98:
            port = find_available_port()
            serve(app, host='localhost', port=port)
