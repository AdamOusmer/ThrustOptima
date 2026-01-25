"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************
"""

import sqlite3 as sql

import pickle


from utilities import scan


class Database:
    database_count: int = 0
    default_name_count: int = 0

    class _Allowed_Class:
        def __init__(self, object=None):
            self._allowed = False

            try:
                self._allow(object)
            except TypeError:
                self._allowed = False
                return

            self._allowed = True

        @staticmethod
        def _allow(test_object):

            if test_object is None:
                return

            if type(test_object) is not dict:
                raise TypeError("The object provided is not a allowed.")

            types = [type(item) for item in test_object.values()]

            if not all([item is scan.Scan for item in types]):
                raise TypeError("The object provided is not a allowed.")

    def __init__(self, name: str = None):
        if name is None or name.strip() is None:
            self._name = "thrustoptima_db" + str(Database.default_name_count) + ".optm"
            Database.default_name_count += 1
            Database.database_count += 1

            self.connect().close()

            return

        self._name = name
        Database.database_count += 1
        self.connect().close()

    def connect(self):
        """
        Connect to the database.
        :return: None
        """
        connect = sql.connect(self._name)
        return connect


