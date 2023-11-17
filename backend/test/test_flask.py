"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the tests for the Flask application using nose2.

"""

import unittest

from backend.src import thrust_optima as flask_app


class ConnectionTesting(unittest.TestCase):

    def test_port(self):
        port1 = flask_app.find_open_port()
        port2 = flask_app.find_open_port()

        self.assertFalse(port1 is not None)
        self.assertFalse(port2 is not None)

        self.assertTrue(isinstance(int, port1))
        self.assertTrue(isinstance(int, port2))
        self.assertFalse(port1 == port2)


if __name__ == "__main__":
    unittest.main()
