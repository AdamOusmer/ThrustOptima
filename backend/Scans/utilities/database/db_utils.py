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


if __name__ == '__main__':
    create()
    insert("test4444", "test4444")
    print(get("test"))
    update("test2", "test")
    print(get("test"))
