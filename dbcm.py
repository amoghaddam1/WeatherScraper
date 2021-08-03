"""
This module holds the context manager which allows for a
more robust connection to the database.
"""

import sqlite3

class DBCM():
    """
    DBCM serves as the context manager for all operations
    with the database.
    """

    def __init__(self, app_database):
        """
        Initializes attributes for the DBCM context manager.
        """
        try:
            self.database_configuration = app_database
            self.conn = None
            self.cursor = None
        except Exception as error:
            print(f"DBCM::__init__::{error}")

    def __enter__(self):
        """
        Executes the setup code to connect to the database.
        """
        try:
            self.conn = sqlite3.connect(self.database_configuration)
            self.cursor = self.conn.cursor()

            return self.cursor
        except Exception as error:
            print(f"DBCM::__enter__::{error}")

    def __exit__(self, exc_type, exc_value, exc_trace):
        """
        Executes the teardown code to close the
        connection to the database.
        """
        try:
            self.conn.commit()
            self.cursor.close()
            self.conn.close()
        except Exception as error:
            print(f"DBCM::__exit__::{error}")
