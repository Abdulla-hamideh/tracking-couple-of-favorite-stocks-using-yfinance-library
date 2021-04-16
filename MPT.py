import pandas as pd
import matplotlib.pyplot as plt
import pandas_datareader as web
import datetime
import os
import yfinance as yf
import numpy as np
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices


stocks = ["AAPL", "MSFT", "AMZN", "TSLA", "NVDA", "FB", "GOOG", "JPM", "NFLX","BA","NKE","WMT","V","PYPL","BAC"]

#Using the pandas-datareader package, we can simply fetch stock data and store the fetched data as CSV files inside a folder:
stock_path = 'stocks'
if not os.path.exists(stock_path):
    os.makedirs(stock_path)

# Fetch some stocks
for symbol in stocks:
    print('Fetching %s...' % symbol)
    start = datetime.datetime(2000, 1, 1)
    #end = datetime.datetime(2020, 6, 30)
    #yahoo or google,google currently not working
    df = web.DataReader(symbol, "yahoo", start)
    df.to_csv(os.path.join(stock_path, '%s.csv' % symbol))


#After running the code, a folder called “stocks” is created and should contain some CSV files.
stock_path = 'stocks'
df = pd.DataFrame()
for file in os.listdir(stock_path):
    # Derive the symbol from the filename
    symbol = file.split('.')[0]

    # Load the data
    path = os.path.join(stock_path, file)
    df_stock = pd.read_csv(path)

    # Set the Date as index column
    df_stock['Date'] = pd.to_datetime(df_stock['Date'])
    df_stock = df_stock.set_index('Date')

    # Resample based on months and compute the changes
    resampled = df_stock.resample('BM')
    monthly = resampled.apply(lambda x: x[-1])
    df[symbol] = monthly['Close'].pct_change()

# Drop NaNs
df = df.dropna()
# Make the plot
x = df.std().tolist()
y = df.mean().tolist()
symbols = df.columns

# Scatterplot and annotation
plt.scatter(x, y)
for index, symbol in enumerate(symbols):
    plt.annotate(symbol, (x[index], y[index]))

# Title and axis
plt.xlabel('Risk')
plt.ylabel('Expected Return')
plt.title('Expected Return versus Risk')
plt.show()


# building optimal porfolio
por = yf.download(stocks, start= "1980-12-12")["Close"]
cov_matrix = por.pct_change().apply(lambda x: np.log(1+x)).cov()

# define weight of the portfolio
def weight(por):
     rand = np.random.random(len(por.columns))
     rand /= rand.sum()
     return rand
# def portfolioreturn(weights):
#     return np.dot(por.mean(),weights)
# def portfoliostd(weights):
#     return(np.dot(np.dot(por.cov(),weights),weights))**(1/2)*np.sqrt(250)


# Yearly returns for individual companies
ind_er = por.resample('Y').last().pct_change().mean()
#random weight or specify it but should add up to 1
print("*"*20+"random or your specified weights"+"*"*20)
# custom weight
# w = [0.1, 0.2, 0.5, 0.2]
port_returns = (weight(por)*ind_er).sum()
print(port_returns)
# Volatility is given by the annual standard deviation. We multiply by 250 because there are 250 trading days/year.
ann_sd = por.pct_change().apply(lambda x: np.log(1+x)).std().apply(lambda x: x*np.sqrt(250))
# Creating a table for visualising returns and volatility of assets
assets = pd.concat([ind_er, ann_sd], axis=1)
assets.columns = ['Returns', 'Volatility']
p_ret = [] # Define an empty array for portfolio returns
p_vol = [] # Define an empty array for portfolio volatility
p_weights = [] # Define an empty array for asset weights

num_assets = len(por.columns)
num_portfolios = 10000
for portfolio in range(num_portfolios):
    weights = np.random.random(num_assets)
    weights = weights/np.sum(weights)
    p_weights.append(weights)
    returns = np.dot(weights, ind_er) # Returns are the product of individual expected returns of asset and its
                                      # weights
    p_ret.append(returns)
    var = cov_matrix.mul(weights, axis=0).mul(weights, axis=1).sum().sum()# Portfolio Variance
    sd = np.sqrt(var) # Daily standard deviation
    ann_sd = sd*np.sqrt(250) # Annual standard deviation = volatility
    p_vol.append(ann_sd)
data = {'Returns':p_ret, 'Volatility':p_vol}

for counter, symbol in enumerate(por.columns.tolist()):
    #print(counter, symbol)
    data[symbol+" weight"] = [w[counter] for w in p_weights]
# simulation is saved in this dataframe
portfolios  = pd.DataFrame(data)
#print(portfolios.to_string())

budget = 25000

# idxmin() gives us the minimum value in the column specified.
min_vol_port = portfolios.iloc[portfolios['Volatility'].idxmin()]
print("*"*20+"Min portfolio return"+"*"*20)
print(min_vol_port)
latest_prices= get_latest_prices(por)
dict_min = min_vol_port.to_dict()
del dict_min["Returns"]
del dict_min["Volatility"]
da = DiscreteAllocation(dict_min,latest_prices,total_portfolio_value=budget)
allocation,leftover = da.lp_portfolio()
# changing the dictionary to a list
data_min = {k: [v] for k, v in allocation.items()}
#changing from rows to coloumns
data_min=pd.DataFrame.from_dict(data_min, ).T
#naming the row index
data_min.columns= ["Shares"]
print(data_min)
#print("Discrete allocation:", allocation)
print("funds Remaining:","$", leftover)

print("*"*80)

rf = 0.01 # risk factor
# Finding the optimal portfolio
optimal_risky_port = portfolios.iloc[((portfolios['Returns']-rf)/portfolios['Volatility']).idxmax()]
print("*"*20+"Maximum return portfolio"+"*"*20)
print(optimal_risky_port)
plt.subplots(figsize=(10, 10))
plt.scatter(portfolios['Volatility'], portfolios['Returns'],marker='o', s=10, alpha=0.3)
plt.scatter(min_vol_port[1], min_vol_port[0], color='r', marker='*', s=500)
plt.scatter(optimal_risky_port[1], optimal_risky_port[0], color='g', marker='*', s=500)
plt.show()

dict_max = optimal_risky_port.to_dict()
# deleting the 2 coloumns for the allocation shares in the portfolio
del dict_max["Returns"]
del dict_max["Volatility"]
da = DiscreteAllocation(dict_max,latest_prices,total_portfolio_value=budget)
allocation,leftover = da.lp_portfolio()
# changing the dictionary to a list
data_max = {k: [v] for k, v in allocation.items()}
#changing from rows to coloumns
data_max=pd.DataFrame.from_dict(data_max, ).T
#naming the row index
data_max.columns= ["Shares"]
print(data_max)
# print("Discrete allocation:", allocation)
print("funds Remaining:","$", leftover)