"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the Database class.

All scans will be transform into binaries using pickles and linked to a name
defined by the user when creating a new scan. All the data will be stored in an .optm
file and save into an sqlite3 database.
"""

import sqlite3
import pickle

import sys


class Database:

    def __init__(self, path: str = "", allowed_class: type = None):

        if not path.strip() or path is None:
            raise ValueError("self._path cannot be empty")

        if allowed_class is None:
            raise ValueError("allowed_class cannot be None")

        self._path = path
        self._allowed_class = allowed_class

    def create(self):
        """
        This function will create the database if it does not exist
        """
        database = sqlite3.connect(self._path)
        cursor = database.cursor()

        try:
            cursor.execute("CREATE TABLE scans (name TEXT, data BLOB)")
        except sqlite3.OperationalError:
            pass

        database.commit()
        database.close()
        print("Database initialized", file=sys.stdout)
        sys.stdout.flush()

    def insert(self, data, name: str = None):
        """
        This function will insert a new scan into the database
        :param data: the data to be saved
        :param name: the name of the scan object
        """
        if not name.strip() or name is None:
            raise ValueError("Name cannot be empty")

        database = sqlite3.connect(self._self._path)
        cursor = database.cursor()

        cursor.execute("INSERT INTO scans VALUES (?, ?)", (name, pickle.dumps(data)))
        database.commit()
        database.close()

    def update(self, data, name: str = None):
        """
        This function will update an existing scan in the database
        :param data: the new data to be saved
        :param name: the name of the old scan object
        """
        if not name.strip() or name is None:
            raise ValueError("Name cannot be empty")

        database = sqlite3.connect(self._path)
        cursor = database.cursor()

        cursor.execute("UPDATE scans SET data = ? WHERE name = ?", (pickle.dumps(data), name))
        database.commit()
        database.close()

    def get(self, name: str = None):
        """
        This function will return the data of a scan object based on its name
        :param name: name of the scan object to be retrieved
        :return: Scan: the scan object
        """

        if not name.strip() or name is None:
            raise ValueError("Name cannot be empty")

        database = sqlite3.connect(self._path)
        cursor = database.cursor()

        cursor.execute("SELECT data FROM scans WHERE name = ?", (name,))
        data = cursor.fetchone()[0]
        database.close()

        loaded = pickle.loads(data)

        if isinstance(loaded, self._allowed_class):
            print("Loaded")
            sys.stdout.flush()
            return loaded

        print("Not recognized", sys.stderr)
        sys.exit(1)

    def get_all_scans(self):
        """
        This function will return an array of the names of the current saved scans
        :return: List: List of all the scans' names
        """

        database = sqlite3.connect(self._path)
        cursor = database.cursor()

        cursor.execute("SELECT ALL name FROM scans")
        data = cursor.fetchall()
        database.close()

        return data
