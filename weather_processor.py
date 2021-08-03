"""
This module holds WeatherProcessor, launches the application and manages all
tasks between the different modules that make up the application.
"""

from datetime import date
from db_operations import DBOperations
from scrape_weather import WeatherScrapper
from plot_operations import PlotOperations

class WeatherProcessor():
    """
    WeatherProcessor manages all operations between the database,
    WeatherScrapper, and PlotOperations.
    """

    def __init__(self):
        """
        Initializes WeatherProcessor.
        """
        try:
            self.db = DBOperations()
            self.scrapper = WeatherScrapper()
            self.plotter = PlotOperations()

            self.months_list = [
                "Brumaire",
                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"
            ]

        except Exception as error:
            print(f"WeatherProcessor::__init__::{error}")

    def update(self):
        """
        Updates the database based on the current date and last entry in database.
        """
        try:
            year = date.today().year
            month = date.today().month

            most_recent_date_in_database = self.db.most_recent_date()[0].split("-")

            last_year_in_database = int(most_recent_date_in_database[0])
            last_month_in_database = int(most_recent_date_in_database[1])
            last_day_in_database = int(most_recent_date_in_database[2])

            final_month = last_year_in_database == year and last_month_in_database == month

            while not final_month:
                try:
                    print(f"Downloading data from {self.months_list[month]} {year}...")
                    weather = self.scrapper.retrieve_montly_data(year, month)

                    if month == 1:
                        month = 12
                        year = year - 1
                    else:
                        month = month - 1

                    final_month = last_year_in_database == year and last_month_in_database == month

                    self.db.save_data(weather)

                except Exception as error:
                    print(f"WeatherProcessor::update::while_loop::{error}")

            print(f"Updating data for {self.months_list[month]} {year}...")

            weather = self.scrapper.retrieve_montly_data(year, month)

            non_duplicates = {}

            for key, value in weather.items():
                try:
                    day = int(key.split("-")[2])
                    if day > last_day_in_database:
                        non_duplicates[key] = value
                except Exception as error:
                    print(f"WeatherProcessor::update::for_loop::{error}")

            self.db.save_data(non_duplicates)

            print("Update complete! Database is now up to date!")


        except Exception as error:
            print(f"WeatherProcessor::update::{error}")

    def retrieve_all(self):
        """
        Purges the database and performs a full download to the database.
        """
        try:
            self.db.purge_data()
            self.db.initialize_db()

            year = date.today().year
            month = date.today().month

            is_finished = False

            while not is_finished:
                try:
                    print(f"Downloading data from {self.months_list[month]} {year}...")
                    weather = self.scrapper.retrieve_montly_data(year, month)
                    if month == 1:
                        month = 12
                        year = year - 1
                    else:
                        month = month - 1

                    is_finished = self.scrapper.same_month()

                    if is_finished:
                        print(
                            f"Data from {self.months_list[month + 1]} {year} "
                            "and after is not available, download complete!"
                        )
                    else:
                        self.db.save_data(weather)
                except Exception as error:
                    print(f"WeatherProcessor::retrieve_all::while_loop::{error}")

        except Exception as error:
            print(f"WeatherProcessor::retrieve_all::{error}")

    def line_plot(self, month, year):
        """
        Retrieves data from the database and passes it
        to instance of PlotOperations.
        """
        try:
            start_date = f"{year}-{month}-01"

            end_date = f"{year}-{month}-31"

            entries = self.db.fetch_data(start_date, end_date)

            timestamps = [entry[0] for entry in entries]
            temperatures = [entry[1] for entry in entries]

            month_string = self.months_list[int(month)]

            self.plotter.line_plot(temperatures, timestamps, year, month_string)

        except Exception as error:
            print(f"WeatherProcessor::line_plot::{error}")

    def box_plot(self, start_year, end_year):
        """
        Retrieves data from the database and passes it
        to instance of PlotOperations
        """
        try:
            weather_data = [[],[],[],[],[],[],[],[],[],[],[],[]]

            start_date = f"{start_year}-01-01"
            finish_date = f"{end_year}-12-31"

            entries = self.db.fetch_data(start_date, finish_date)

            for entry in entries:
                try:
                    month = entry[0].split("-")[1]

                    if month == "01":
                        weather_data[0].append(entry[1])

                    if month == "02":
                        weather_data[1].append(entry[1])

                    if month == "03":
                        weather_data[2].append(entry[1])

                    if month == "04":
                        weather_data[3].append(entry[1])

                    if month == "05":
                        weather_data[4].append(entry[1])

                    if month == "06":
                        weather_data[5].append(entry[1])

                    if month == "07":
                        weather_data[6].append(entry[1])

                    if month == "08":
                        weather_data[7].append(entry[1])

                    if month == "09":
                        weather_data[8].append(entry[1])

                    if month == "10":
                        weather_data[9].append(entry[1])

                    if month == "11":
                        weather_data[10].append(entry[1])

                    if month == "12":
                        weather_data[11].append(entry[1])

                except Exception as error:
                    print(f"WeatherProcessor::box_plot::for_loop::{error}")

            self.plotter.box_plot(weather_data, start_year, end_year)

        except Exception as error:
            print(f"WeatherProcessor::box_plot::{error}")

if __name__ == '__main__':
    try:
        app = WeatherProcessor()

        app.db.initialize_db()

        print()
        print("*************************************************")
        print("*                                               *")
        print("* Ali's Stupendous Weather Processor            *")
        print("*                                               *")
        print("* Version 1.0                                   *")
        print("* Developed by Ali Moghaddam                    *")
        print("* Copywrong 2021                                *")
        print("*                                               *")
        print("*************************************************")
        print()
        print("Hello There! Let's get started!")

        if app.db.count_rows_in_table()[0] == 0:
            print()
            print(
                "We see you don't have any data for plotting. "
                "In order for this application to work,\n"
                "you need some data. So we're gonna have to do a "
                "full download.\n"
            )
            input(
                "This can take a few minutes. When you're ready, "
                "press enter to begin: "
            )
            print()
            app.retrieve_all()
        else:
            while True:
                print()
                user_input = input(
                    "Would to perform a [F]ull Download, "
                    "[U]pdate, or [S]kip to begin plotting data?: "
                ).lower()

                if user_input in ("f", "full", "full download"):
                    print()
                    user_input = input(
                        "WARNING: A FULL DOWNLOAD TAKES A FEW MINUTES. "
                        "Are you sure that's what you want? [Y]es or [N]o: "
                    ).lower()

                    if user_input in ("y", "yes"):
                        print()
                        app.retrieve_all()
                        break

                if user_input in ("u", "update"):
                    print()
                    app.update()
                    break

                if user_input in ("s", "skip"):
                    break

        while True:
            print()
            user_input = input(
                "Would you like to plot [D]aily average temperatures, "
                "[M]onthly average temperatures, or [E]xit the program?: "
            ).lower()

            if user_input in ("d", "daily"):
                print()

                year_to_plot = input("Enter Year(YYYY): ")
                month_to_plot = input("Enter Month(MM): ")

                app.line_plot(month_to_plot, year_to_plot)

                print()
                user_input = input(
                    "Would you like to [E]xit the program, "
                    "or [G]enerate another graph?: "
                ).lower()

            if user_input in ("m", "monthly"):
                print()

                start_year_to_plot = input("Enter start date(YYYY): ")
                end_year_to_plot = input("Enter end date(YYYY): ")

                app.box_plot(start_year_to_plot, end_year_to_plot)

                print()
                user_input = input(
                    "Would you like to [E]xit the program, "
                    "or [G]enerate another graph?: "
                ).lower()

            if user_input in ("e", "exit"):
                break

        print()
        print("Good Bye!")
        print()

    except Exception as error:
        print(f"weather_processor::main::{error}")
