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

path = "data.optm"


def create():
    database = sqlite3.connect(path)
    cursor = database.cursor()

    try:
        cursor.execute("CREATE TABLE scans (name TEXT, data BLOB)")
    except sqlite3.OperationalError:
        pass

    database.commit()
    database.close()
    print("Database initialized", file=sys.stdout)
    sys.stdout.flush()


def insert(data, name: str = None):
    if not name.strip() or name is None:
        raise ValueError("Name cannot be empty")

    database = sqlite3.connect(path)
    cursor = database.cursor()

    cursor.execute("INSERT INTO scans VALUES (?, ?)", (name, pickle.dumps(data)))
    database.commit()
    database.close()


def update(data, name: str = None):
    if not name.strip() or name is None:
        raise ValueError("Name cannot be empty")

    database = sqlite3.connect(path)
    cursor = database.cursor()

    cursor.execute("UPDATE scans SET data = ? WHERE name = ?", (pickle.dumps(data), name))
    database.commit()
    database.close()


def get(name: str = None):
    if not name.strip() or name is None:
        raise ValueError("Name cannot be empty")

    database = sqlite3.connect(path)
    cursor = database.cursor()

    cursor.execute("SELECT data FROM scans WHERE name = ?", (name,))
    data = cursor.fetchone()[0]
    database.close()

    return pickle.loads(data)


def get_all_scans():
    """
    This function will return an array of the current saved scans
    :return: List: List of all the scans
    """

    database = sqlite3.connect(path)
    cursor = database.cursor()

    cursor.execute("SELECT ALL name FROM scans")
    data = cursor.fetchall()
    database.close()

    return data


if __name__ == '__main__':
    pass
