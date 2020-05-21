from requests import get
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import time
from scipy import stats
import csv


#Returns wheether the input is a valid trading day
def valid_trading_day(date):
    url = "https://bigcharts.marketwatch.com/historical/default.asp?symb=AAPL&closeDate={month}%2F{day}%2F{year}".format(month=date.month, day=date.day, year=date.year)   
    content = get(url)
    if (content.text.find("No data for") != -1):
        return False
    return True


#Finds closing price based on ticker/date
def closing_price(ticker, date):
    if not isinstance(date, dt.date):
        return("Enter valid date")
    if valid_trading_day(date):
        url = "https://bigcharts.marketwatch.com/historical/default.asp?symb={ticker}&closeDate={month}%2F{day}%2F{year}".format(ticker=ticker, month=date.month, day=date.day, year=date.year)    
        content = get(url)
        index = content.text.find("Closing Price:")
        closing = (content.text[index+35:index+55])
        closing_price = float(closing.split("<td>")[1].split("</td>")[0])
        return float(closing_price)
    else:
        return("Enter valid date")


#Finds the nearest trading day if the given date is not valid
def nearest_trading_day(date):
    if valid_trading_day(date):
        return date
    one_day = dt.timedelta(days=1)
    while not valid_trading_day(date):
        date = date + one_day
    return date


#Stock price change in stock value given start date and time interval
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



#First dataset of insider trading, 4/8/2020
start1 = dt.date(2020, 4, 8)
url1 = 'https://www.reddit.com/r/StockMarket/comments/fx9a62/significant_insider_trading_activity_last_7_days/'


#Second dataset of insider trading, 1/14/2019
start2 = dt.date(2019, 1, 14)
url2 = 'https://www.reddit.com/r/StockMarket/comments/afz2fw/significant_insider_trading_activity_last_7_days/'


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

# data = fetch_data('https://www.reddit.com/r/StockMarket/comments/fx9a62/significant_insider_trading_activity_last_7_days/')
# data['Company'] = data['Company'].map(lambda x: x.split(' / ')[0])

# start3 = dt.date(2015, 10, 15)
# data = collect_data_std("KO", start3)
# print(data)


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


# def percent_neg(input):
#     return 1 - percent_pos(input)



data = read_input('selling_v1.csv')
# print(percent_neg(data))