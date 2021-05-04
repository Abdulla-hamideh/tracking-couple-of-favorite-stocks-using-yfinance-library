import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
from datetime import date

stocks = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA", "FB", "GOOG", "JPM", "NFLX","BA","NKE","WMT","V","PYPL","BAC"]

today = date.today()
first = dt.datetime(day=1,month=1,year=2008)
first = first.strftime('%Y-%m-%d')


# the fast mA window size
short_window = 50

# the slow Ma window size
long_window = 200

for i in stocks:
    # getting the ticker
    ticker = yf.Ticker(i)
    #' getting the history for the ticker
    hist = ticker.history(start=first,end=today)
    # definig the short and long
    short_Ma = pd.DataFrame()
    Long_Ma = pd.DataFrame()
    short_Ma["Close"] = hist["Close"].rolling(window=short_window).mean()
    Long_Ma["Close"] = hist["Close"].rolling(window=long_window).mean()
    x= (short_Ma["Close"]> Long_Ma["Close"]).astype(int)
    y= x.diff()
    crossoversignal = pd.DataFrame()
    crossoversignal[i]=hist["Close"]
    crossoversignal["buy"] = hist["Close"][y>0]
    crossoversignal["sell"] = hist["Close"][y<0]
    print("*"*20,i,"*"*20)
    # buy signal in the exact date
    print(y[y>0])
    # sell sinal n the exact date
    print(y[y<0])
    plt.plot(hist["Close"], label = i)
    plt.plot(short_Ma["Close"], label = "Short MA")
    plt.plot(Long_Ma["Close"],label= "Long MA")
    plt.scatter(crossoversignal["buy"].index,crossoversignal["buy"], label= "buy", color = "green")
    plt.scatter(crossoversignal["sell"].index,crossoversignal["sell"], label= "sell", color = "red")
    plt.legend()
    plt.title(i)
    plt.show()

