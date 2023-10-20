"""
******************************************************************
Copyright Adam Ousmer for Space Concordia - Rocketry Division 2023
All Rights Reserved.
******************************************************************

This module contains the definition of the Database class.

# TODO: Add docstrings
"""


class Database:

    def _init_(self, name: str = None, path: str = None):
        self.data_count = 0

        if not name.strip() or name.lower() == "default":
            raise ValueError("Name cannot be empty or 'default'")

        self._name = name if name is not None else f"default_{self.data_count}"
        self.id = f"thrust_optima_{name}_{self.data_count}"

        if not path.strip() or path is None:
            raise ValueError("No defined path for the database in the system. Please contact the administrator.")

    def write_infos(self, table: str = None, data: tuple = None):
        """
        :raises ValueError: If the table name or the data is empty or None.
        """

        if not table.strip() or table is None:
            raise ValueError("Invalid table name.")

        if data is None:
            raise ValueError("invalid data name")
