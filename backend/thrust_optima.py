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

from Scans.scans_controller import Controller
from Scans.utilities.database.db_utils import Database as Db

import pickle
import json
import time

from flask import Flask
from waitress import serve

import sys
import socket

app = Flask(__name__)  # Flask application
controller = Controller()  # Controller object of the scans module
port = 5000  # Default port (We will find an open port when the server is launched)
db = Db("data.optm", Controller)  # Database object


@app.route('/')
def index():
    """
    Main server endpoint. This function needs to be called when the user launches the application.

    This function will initialize the database.
    :return: String: "Server Launched"
    """
    db.create()
    print("Database initialized", file=sys.stdout)
    sys.stdout.flush()

    return "Server Launched"


@app.route('/load', methods=['GET'])
def load(name: str = None):
    """
    This function will load an existing scan from the database.
    :raises ValueError: If the name is empty or None
    """

    global controller

    if not name.strip() or name is None:
        raise ValueError("Path cannot be empty")

    controller = pickle.load(db.get(name))

    return "Loaded"


@app.route('/list', methods=['GET'])
def list_scans():
    """
    This function will return a json parsed array of all the scans in the database.
    """

    scans = db.get_all_scans()

    return json.dumps(scans)


@app.route('/cleanup', methods=['POST'])
def close():
    """
    Exit point of the program. This function will be called when the user closes the program to ensure that all
    resources are properly closed and saved.
    :return: None
    """
    global controller

    print("Closing...")
    sys.stdout.flush()

    # TODO: do the cleanup here

    return "Closed"


def find_open_port():
    """
    This function will find a port on the localhost that is opened and handle http requests.
    It will print it in the stdout to be processed by the frontend.
    :return: Integer: port
    """
    global port

    # Add a filter to only get the open ports that handle http requests
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    sock.bind(('localhost', 0))  # Bind the socket to the localhost and a random port
    port = sock.getsockname()[1]

    print(f"port={port}")  # send the port to the frontend through the stdout
    sys.stdout.flush()

    return port  # return the port if needed


if __name__ == '__main__':
    """
    Main entry point of the backend. This function will be called when the user launches the program.
    
    This function will find an available port to start the WSGI server and will launch the Flask application.
    
    :raises OSError: If the port is already occupied
    """

    find_open_port()

    try:
        # Wait for the port to be printed in the stdout and processed by the frontend. It is just a safety measure.
        time.sleep(1)
        print("Starting server...", file=sys.stdout)  # Used by the frontend to know when the server is ready
        sys.stdout.flush()

        serve(app, host='localhost', port=port)  # Start the WSGI server and serve the Flask application
    except OSError as e:
        if e.errno == 98:
            find_open_port()  # Find another port if the previous one is already occupied

            time.sleep(1)

            print("Starting server...", file=sys.stdout)
            sys.stdout.flush()

            serve(app, host='localhost', port=port)
