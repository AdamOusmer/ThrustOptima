"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************
"""

from flask import Flask
from waitress import serve

import sys
import socket

import app.api
from features import loader


class Application:
    def __init__(self):
        self.app = Flask(__name__)
        self.port = Application._open_port()

    def run(self):
        serve(self.app, host='localhost', port=self.port)

    @staticmethod
    def _open_port():
        """
        This function will find a port on the localhost that is opened and handle http requests.
        It will print it in the stdout to be processed by the frontend.
        :return:Integer: port
        """

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Socket that handle http requests

        sock.bind(('localhost', 0))  # Bind the socket to the localhost and a random port
        port = sock.getsockname()[1]

        sock.close()

        return port

    def get_port(self):
        return self.port


def start():
    """
    Main entry point of the backend. This function will be called when the user launches the program.
    This function will find an available port to start the WSGI server and will launch the Flask application.

    :raises OS Error: If the port is already occupied
    """
    app = Application()

    print(f"port={app.get_port()}")  # send the port to the frontend through the stdout
    sys.stdout.flush()

    app.run()


if __name__ == '__main__':
    start()
