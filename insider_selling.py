from requests import get
# from bs4 import BeautifulSoup4
import pandas as pd
import datetime as dt
import time
from scipy import stats
import yfinance as yf
import csv

# UTILITY FUNC

# Returns whether input is valid trading day
def valid_trading_day(date):
    url = "https://bigcharts.marketwatch.com/historical/default.asp?symb=AAPL&closeDate={month}%2F{day}%2F{year}".format(month=date.month, day=date.day, year=date.year)   
    content = get(url)
    if (content.text.find("No data for") != -1):
        return False
    return True

# Closing price based on ticker and date
def closing_price(ticker, date):
    if not isinstance(date, dt.date):
        return("Enter valid date")
    if valid_trading_day(date):
        date = "{year}-{month}-{day}".format(year=date.year, month=date.month, day=date.day)
        return yf.Ticker(ticker).history(period="max").loc[date].loc["Close"]
    else:
        return("Enter valid date")

# Finds the nearest trading day if the given date is not valid
def nearest_trading_day(date):
    if valid_trading_day(date):
        return date
    one_day = dt.timedelta(days=1)
    while not valid_trading_day(date):
        date = date + one_day
    return date

# Stock price change in stock value given start date and time interval
def price_change(ticker, start, delta):
    nearest_start = nearest_trading_day(start)
    nearest_end = nearest_trading_day(start + delta)
    return int(closing_price(ticker, nearest_end) - closing_price(ticker, nearest_start))

#Percent change in stock over delta
def percent_change(ticker, start, delta):
    nearest_start = nearest_trading_day(start)
    nearest_end = nearest_trading_day(start + delta)
    change = closing_price(ticker, nearest_end) - closing_price(ticker, nearest_start)
    return (change / closing_price(ticker, nearest_start))


# DATASET


# First dataset of insider trading, 1/14/2019
start2 = dt.date(2020, 3, 23)
buying1 = pd.read_csv("Buy 1_14_19.csv")
print(percent_change("TSLA", start2, dt.timedelta(weeks=52)))

print(buying1)



#Find insider buying/selling data from reddit, convert to pandas DataFrame
def fetch_data(url):
    try:
        tables = pd.read_html(url)
        insider_buying = tables[0]
        insider_selling = tables[1]
        return insider_selling
    except:
        return fetch_data(url)


# Return a list with the percent change 13, 26, and 52 weeks after date
def collect_data(ticker, start):
    lst = []
    time_delta = dt.timedelta(weeks=13)
    for i in range(3):
        change = percent_change(ticker, start, time_delta)
        lst.append(change)
        time_delta *= 2
    return lst


# Return a list of percent change standardized to market move, difference in security movement vs overall market movement
def collect_data_std(ticker, start):
    lst = []
    time_delta = dt.timedelta(weeks=13)
    for i in range(3):
        change = percent_change(ticker, start, time_delta)
        market = percent_change("SPY", start, time_delta)
        lst.append(change - market)
        time_delta *= 2
    return lst



# Checking validity of previous functions



# Takes input data and returns array of tuples (insider_magnitude: security_change)
def read_input(csv_file):
    reader = csv.reader(open("selling_v1.csv", newline=''))
    lst_instances = []
    for row in reader:
        if reader.line_num > 2:
            lst_instances.append((float(row[1]), float(row[2])))
    
    return lst_instances


def percent_pos(input):
    positive = 0
    total = len(input)
    for i in input:
        if i[1] > 0:
            positive += 1
    return float(positive / total)


def percent_neg(input):
    return 1 - percent_pos(input)



# data = read_input('selling_v1.csv')
# print(percent_neg(data))