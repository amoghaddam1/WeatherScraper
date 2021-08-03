"""
This module holds PlotOperations which employees matplotlib
to graph weather data.
"""

import matplotlib.pyplot as plt

class PlotOperations:
    """
    Graphs climate data dependant on the vector
    data passed to each method.
    """

    def box_plot(self, data, start_year, end_year):
        """
        Graphs a box plot of mean temperatures
        in a date range supplied by the user.
        """
        try:
            plt.boxplot(data)
            title = f"Monthly Temperature Distribution for: {start_year} to {end_year}"

            plt.title(title)
            plt.xlabel("Month")
            plt.ylabel("Temperature (Celsius)")

            plt.show()

        except Exception as error:
            print(f"PlotOperations::box_plot::{error}")

    def line_plot(self, average_temperatures, timestamps, year, month):
        """
        Graphs a line plot of mean temperature data for a
        particular month based on user input.
        """
        try:
            title = f"Daily Average Temperatures for: {month} {year}"

            plt.title(title)
            plt.ylabel("Average Temperature")
            plt.xlabel("Day of Month")

            plt.plot(timestamps, average_temperatures)

            plt.xticks(timestamps, rotation=-45, fontsize=8)

            plt.tight_layout()
            plt.show()

        except Exception as error:
            print(f"PlotOperations::line_plot::{error}")
