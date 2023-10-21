"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************
"""
from thrust_optima import app
from waitress import serve

import sqlite3

import sys
import socket


def find_available_port():
    """
    This function will find an available port to run the server on.
    :return: The port number
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(('', 0))
    port = sock.getsockname()[1]
    sock.close()

    return port


def update_port(new_port: int):
    """
    This function will update the port number in the database.
    :param new_port: The port number to update
    :return: None
    """

    conn = sqlite3.connect("../database.optm")
    pointer = conn.cursor()

    pointer.execute("UPDATE settings SET value = ? WHERE name = ?", (new_port, "port"))

    conn.commit()
    conn.close()


if __name__ == '__main__':
    print("Starting server...", file=sys.stdout)
    sys.stdout.flush()
    try:
        serve(app, host='localhost', port=5000)
    except OSError as e:
        if e.errno == 98:
            port = find_available_port()
            update_port(port)
            serve(app, host='localhost', port=port)
