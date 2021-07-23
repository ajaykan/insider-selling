import requests
import requests_html
import json
import io
import ftplib
import feedparser
import pandas as pd
import datetime as dt
import time
import statistics as stat
import matplotlib.pyplot as plt
import csv
import os
from yahoo_fin import stock_info as si


# CLASS

class Dataset: 

    """
    Populates a Dataset object with all the relevant meta data (filename, data table, buy/sell, date)
    Contain all relevant functions for analysis
    Allow for easy iteration of datasets
    Following instance attributes: filename, data, buy, date

    Filename structure: '(Buy/Sell)-(MM)_(DD)_(YYYY).csv' -> ex. 'Buy-01_14_2019.csv' 
    """

    def __init__(self, filename, underlying="SPY", deltas=[3, 6, 12]):
        self.filename = filename
        try:
            table = pd.read_csv(self.filename)
            self.data = table
        except FileNotFoundError:
            print("Invalid filename")
        
        temp_name = self.filename
        temp_name = temp_name.split("-")
        if temp_name[0].split("/")[1] == "Buy":
            self.buy = True
        elif temp_name[0].split("/")[1] == "Sell":
            self.buy = False
        else:
            print("Invalid filename")

        date = temp_name[1].removesuffix(".csv").split("_")
        self.date = dt.date(int(date[2]), int(date[0]), int(date[1]))

        self.deltas = deltas
        self.underlying = underlying
        self.comparison_performance = None

        self.data_points = None # returns list of tuples [(avg returns, magnitude)]

        # meta data
        self.avg_deviation = 0
        self.ratio_win_lose = 0


    def set_deltas(self, deltas):
        assert(type(deltas) == list)
        self.deltas = deltas

    def set_comparison(self, ticker):
        assert(type(ticker) == str)
        self.underlying = ticker
    
    def generate_data(self, print_errors=False):
        lst = []
        for i in range(len(self.data.index)):
            try:
                ticker = self.data.loc[i, "Company"]
                ticker = ticker.split("/")[0][:-1]
                
                magnitude = self.data.loc[i, "Value Change"]
                pct_changes = [get_delta(ticker, self.date, dt.timedelta(weeks=j*4), pct=True) for j in self.deltas]
                standardized_returns = [round(pct_changes[i]/self.comparison_performance[i], 4) for i in range(len(self.deltas))]
                if self.buy:
                    lst.append((round(stat.mean(standardized_returns), 4), remove_commas(magnitude)))
                else:
                    lst.append((round(-1*stat.mean(standardized_returns), 4), remove_commas(magnitude)))
            except (KeyError, AssertionError):
                if print_errors:
                    print("Error with ticker: {0}".format(ticker))

        self.data_points = lst

    def generate_visualization(self):
        x_val = [x[0] for x in self.data_points]
        y_val = [y[1] for y in self.data_points]
        plt.plot(x_val, y_val)
        plt.show()

    def generate_avg_deviation(self):
        self.avg_deviation = stat.mean([x[0] for x in self.data_points])

    def generate_ratio_win_lose(self):
        total_win = sum([x[0] > 0 for x in self.data_points])
        self.ratio_win_lose = total_win / len(self.data_points)

    def update(self, timer=False, print_errors=False): # can specify whether to print time to run, errored tickers
        start = time.time()
        self.comparison_performance = [get_delta(self.underlying, self.date, dt.timedelta(weeks=i*4), pct=True) for i in self.deltas]
        self.generate_data(print_errors)
        self.generate_avg_deviation()
        self.generate_ratio_win_lose()
        end = time.time()
        if timer:
            print("Second to run: " + str(round(end-start, 2)))

    def __str__(self):
        self.update()
        print("---")
        print("Insider {0}ing on {1}".format("buy" if self.buy else "sell", dateobj_to_str(self.date)))
        print("Underlying comparator: {0}".format(self.underlying))
        print("Deltas: {0} (months)".format(self.deltas))
        print("Comparison performance: {0}: ".format([str(round(i, 4)*100)+"%" for i in self.comparison_performance]))
        print("Performance Data:")
        print("Average deviation: {0}".format(str(self.avg_deviation)))
        print("Ratio of win/lose: {0}".format(str(self.ratio_win_lose)))
        return "---"


# UTILITY FUNCTIONS

def remove_commas(string): # remove commas from a str, returns int
    num = string.replace(",", "")
    return float(num)


def dateobj_to_str(date):
    assert(type(date) == dt.date)
    string = ""
    if date.month < 10:
        string += "0" + str(date.month)
    else:
        string += str(date.month)
    string += "/"
    if date.day < 10:
        string += "0" + str(date.day)
    else:
        string += str(date.day)
    string += "/"
    string += str(date.year)
    return string


def get_delta(ticker, start_date, delta, pct=True): # date is dt object, delta is dt.timedelta obj, return change in price or percent
    assert(type(start_date) == dt.date)
    assert(type(delta) == dt.timedelta)
    if start_date > dt.date.today():
        return "Invalid start date"
    end_date = start_date + delta
    if end_date > dt.date.today():
        return "Invalid delta"

    end_date = dateobj_to_str(end_date)
    start_date = dateobj_to_str(start_date)
    tbl = si.get_data(ticker, start_date=start_date, end_date=end_date, interval="1d")
    
    start = tbl["open"][0]
    end = tbl["close"][-1]
    price_change = end - start
    if pct:
        return price_change / start
    else:
        return price_change


# WORKSPACE

buying1 = Dataset('Data/Buy-04_08_2020.csv')
selling1 = Dataset('Data/Sell-10_23_2020.csv')

# buying1.set_comparison("SPY")
# buying1.set_deltas([3, 6])
# buying1.update()

# print(buying1.data_points)

# selling1.set_comparison("SPY")
# selling1.set_deltas([3, 6])
# selling1.update()

# print(selling1.data_points)


root_dir = '/Users/ajayk/Documents/Projects/Python/ULAB_insider_selling/Data'


# PARSING THROUGH EAACH FILE IN DATA

def parse_data_folder():
    buy_data = []
    sell_data = []
    for subdir, dirs, files in os.walk(root_dir):
        for file in files:
            try:
                x = Dataset("Data/" + file)
                x.set_comparison("SPY")
                if (dt.date.today() - x.date) > dt.timedelta(days=365):
                    x.set_deltas([3, 6, 12])
                else:
                    x.set_deltas([3, 6])
                x.update()
                if x.buy:
                    buy_data.extend(x.data_points)
                    print("Dataset {0} added".format(file))
                else:
                    sell_data.extend(x.data_points)
                    print("Dataset {0} added".format(file))
            except:
                print("Error on file {0}".format(file))
    
    return buy_data, sell_data


buy, sell = parse_data_folder()


