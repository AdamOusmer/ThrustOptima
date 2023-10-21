"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the Database class.

This database will contain all the path to all the individual files. Each file will contain the scans objects
and the sqlite3 database will contain the binary data of the scans. This database will be a .optm file.
"""

import sqlite3
import pickle


database = sqlite3.connect("database.optm")


