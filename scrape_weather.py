"""
This module holds the WeatherScrapper class that is used
to scrape HTML from the Government of Canada website.
"""

from html.parser import HTMLParser
import urllib.request
import ssl

ssl._create_default_https_context = ssl._create_unverified_context

class WeatherScrapper(HTMLParser):
    """
    WeatherScrapper retrieves the climate data (specifically the date, max, min, and mean)
    from the Government of Canada website by scrapping the HTML tables per month.
    """

    def __init__(self):
        """
        Initializes WeatherScrapper by setting the required fields.
        """
        try:
            HTMLParser.__init__(self)

            self.good_data = True

            self.title = None
            self.in_title = False
            self.is_same_month = False

            self.in_tbody = False
            self.in_abbr = False
            self.in_td = False

            self.year = None
            self.month = None

            self.tr_column_count = 3

            self.weather = {}
            self.weather_current_key = None

            self.temps_list = []

        except Exception as error:
            print(f"WeatherScrapper::__init__::{error}")

    def handle_starttag(self, tag, attrs):
        """
        Sets the appropriate flags to True when the
        tag processed is one of tag being looked for.
        """
        try:
            if "title" in tag:
                self.in_title = True

            if "tbody" in tag:
                self.in_tbody = True

            if self.in_tbody:
                if "tr" in tag:
                    self.tr_column_count = 0

                if "abbr" in tag:
                    self.in_abbr = True

                if "td" in tag:
                    self.in_td = True

        except Exception as error:
            print(f"WeatherScrapper::handle_starttag::{error}")

    def handle_data(self, data):
        """
        Handles data by adding it to the weather dictionary if the
        data handled is the data being sought.
        """
        try:
            if self.in_title:
                if data == self.title:
                    self.is_same_month = True

                self.title = data
                self.in_title = False

            if self.in_tbody:
                if "Sum" in data:
                    self.in_tbody = False

                if self.in_abbr:
                    self.weather_current_key = f"{self.year}-{self.month}-{data}"

                if self.in_td and self.tr_column_count != 3:
                    if "M" in data:
                        self.good_data = False
                    elif "E" in data:
                        self.good_data = False
                    else:
                        self.temps_list.append(data)

                    self.tr_column_count = self.tr_column_count + 1

                    if self.tr_column_count == 3:
                        if self.good_data and self.weather_current_key is not None:
                            daily_temps = {}

                            daily_temps["Max"] = self.temps_list[0]
                            daily_temps["Min"] = self.temps_list[1]
                            daily_temps["Mean"] = self.temps_list[2]

                            self.weather[self.weather_current_key] = daily_temps

                        self.temps_list.clear()

                        self.good_data = True

                        self.weather_current_key = None


        except Exception as error:
            print(f"WeatherScrapper::handle_data::{error}")

    def handle_endtag(self, tag):
        """
        Handles end tags by setting the appropriate flags to False.
        """
        try:
            if "tbody" in tag:
                self.in_tbody = False

            if self.in_tbody:
                if "abbr" in tag:
                    self.in_abbr = False

                if "td" in tag:
                    self.in_td = False


        except Exception as error:
            print(f"ColourScrapper::handle_endtag::{error}")

    def retrieve_montly_data(self, year, month):
        """
        Retrieves and returns the max, min, mean, and dates for the requested month as a dictionary.
        """
        try:
            self.weather = {}

            self.month = "{:0>2}".format(month)
            self.year = year

            url = (
                f"https://climate.weather.gc.ca/climate_data/daily_data_e.html"
                f"?StationID=27174&timeframe=2&StartYear=1840&EndYear=2021&Day=29&"
                f"Year={year}&Month={month}#"
            )

            with urllib.request.urlopen(url) as response:
                HTML = str(response.read())

            self.feed(HTML)

            return self.weather

        except Exception as error:
            print(f"MyHTMLParser::print_address::{error}")

    def same_month(self):
        """
        Returns True if the month being processed is the same as the previous month,
        otherwise returns False.
        """
        return self.is_same_month
