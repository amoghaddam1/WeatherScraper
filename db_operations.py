"""
This module holds DBOperations which handles
interactions with the database
"""

from dbcm import DBCM

class DBOperations():
    """
    DBOperations handles interactions with the database.
    """

    def __init__(self):
        """
        Initializes the DBOperations Class.
        """
        self.app_database = "weather.sqlite"

    def fetch_data(self, start_date, finish_date):
        """
        Fetches sample_dates and mean
        temperatures between two dates.
        """
        with DBCM(self.app_database) as cursor:
            try:
                sql_select = (
                    """
                    SELECT sample_date, avg_temp
                    FROM weather
                    WHERE sample_date
                    BETWEEN date(?) AND date(?)
                    """
                )

                dates = [start_date, finish_date]

                cursor.execute(sql_select, dates)

                return cursor.fetchall()

            except Exception as error:
                print(f"DBOperations::fetch_data::{error}")

    def save_data(self, weather_dictionary):
        """
        Extracts dictionary data and saves each "row" to the database.
        """
        with DBCM(self.app_database) as cursor:
            try:
                insert_sql = (
                    """
                    INSERT INTO weather
                    (sample_date, max_temp, min_temp, avg_temp, location)
                    VALUES (?,?,?,?,?)
                    """
                )

                for weather, daily_temps in weather_dictionary.items():
                    try:
                        data = []
                        data.append(weather)
                        for value in daily_temps.values():
                            try:
                                data.append(value)
                            except Exception as error:
                                print(f"DBOperations::save_date::inner for loop::{error}")

                        data.append("Winnipeg, MB")
                        cursor.execute(insert_sql, data)

                    except Exception as error:
                        print(f"DBOperations::save_data::outer for loop::{error}")

            except Exception as error:
                print(f"DBOperations::save_data::main::{error}")

    def initialize_db(self):
        """
        Creates the weather database and table.
        """
        with DBCM(self.app_database) as cursor:
            try:
                cursor.execute(
                    """
                    create table if not exists weather
                    (id integer primary key autoincrement not null,
                    sample_date text not null UNIQUE,
                    location text not null,
                    min_temp real not null,
                    max_temp real not null,
                    avg_temp real not null);
                    """
                )

            except Exception as error:
                print(f"DBOperations::initialize_db::{error}")

    def purge_data(self):
        """
        Drops the weather table from the database.
        """
        with DBCM(self.app_database) as cursor:
            try:
                cursor.execute("""drop table weather;""")

            except Exception as error:
                print(f"DBOperations::purge_data::{error}")

    def count_rows_in_table(self):
        """
        Returns 0 if there are no rows in the table.
        """
        with DBCM(self.app_database) as cursor:
            try:
                cursor.execute("""SELECT COUNT(1) FROM weather;""")
                return cursor.fetchone()

            except Exception as error:
                print(f"DBOperations::count_rows_in_table::{error}")

    def most_recent_date(self):
        """
        Returns the most recent date from the database.
        """
        with DBCM(self.app_database) as cursor:
            try:
                sql_select = (
                    """
                    SELECT MAX(sample_date)
                    FROM weather
                    """
                )

                cursor.execute(sql_select)

                return cursor.fetchone()

            except Exception as error:
                print(f"DBOperations::most_recent_date::{error}")
