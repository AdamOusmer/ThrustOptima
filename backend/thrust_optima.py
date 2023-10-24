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
import pickle

from flask import Flask
from waitress import serve

import sys
import json

from Scans.scans_controller import Controller
import Scans.utilities.database.db_utils as db

app = Flask(__name__)
controller = Controller()
port = 5000


@app.route('/')
def index():
    """
    Entry point of the program
    :return: None
    """
    db.create()
    print("Database initialized", file=sys.stdout)
    sys.stdout.flush()

    db.insert("hi", "test4444")

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

    return "Closed"


def find_open_port():
    """
    This function will return an open port on the localhost and print it in the
    stdout in order to ensure that the application can be launched even when the default
    5000 port is already occupied.
    :return: Integer: port
    """
    global port

    # TODO create the port searching algorithm here.

    print(f"port={port}")

    return port


# Waitress server
if __name__ == '__main__':
    print("Starting server...", file=sys.stdout)
    sys.stdout.flush()
    try:
        serve(app, host='localhost', port=5000)
    except OSError as e:
        if e.errno == 98:
            find_open_port()
            serve(app, host='localhost', port=port)
